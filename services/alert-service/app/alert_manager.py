"""
Manager principal para el servicio de alertas
"""
import logging
import asyncio
import json
import statistics
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import pytz
import httpx
import aioredis
import asyncpg
from collections import defaultdict

from .models import (
    AlertRule, AlertCondition, AlertAction, AlertExecution, VariableData,
    ExecutionStatus, AlertStatus, ConditionOperator, ConditionFunction
)

logger = logging.getLogger(__name__)
CHILE_TZ = pytz.timezone('America/Santiago')


class AlertManager:
    """
    Manager principal para manejar todas las operaciones de alertas
    """
    
    def __init__(self, database_url: str, redis_url: str, django_api_url: str, 
                 notification_service_url: str, telemetry_service_url: str):
        self.database_url = database_url
        self.redis_url = redis_url
        self.django_api_url = django_api_url
        self.notification_service_url = notification_service_url
        self.telemetry_service_url = telemetry_service_url
        
        # Conexiones
        self.db_pool: Optional[asyncpg.Pool] = None
        self.redis: Optional[aioredis.Redis] = None
        self.http_client: Optional[httpx.AsyncClient] = None
        
        # Cache de variables
        self.variable_cache: Dict[str, List[VariableData]] = defaultdict(list)
        self.cache_ttl = 3600  # 1 hora
        
        # Scheduler para ejecuciones periódicas
        self.scheduler_task: Optional[asyncio.Task] = None
    
    async def initialize(self):
        """Inicializar conexiones y scheduler"""
        try:
            # Pool de base de datos
            self.db_pool = await asyncpg.create_pool(self.database_url)
            logger.info("Database pool created")
            
            # Redis para cache y coordinación
            self.redis = aioredis.from_url(self.redis_url)
            await self.redis.ping()
            logger.info("Redis connection established")
            
            # Cliente HTTP
            self.http_client = httpx.AsyncClient(timeout=30.0)
            logger.info("HTTP client initialized")
            
            # Iniciar scheduler
            self.scheduler_task = asyncio.create_task(self._scheduler_loop())
            logger.info("Alert scheduler started")
            
        except Exception as e:
            logger.error(f"Error initializing alert manager: {e}")
            raise
    
    async def health_check(self) -> Dict[str, str]:
        """Verificar salud de las conexiones"""
        connections = {}
        
        try:
            # Verificar base de datos
            if self.db_pool:
                await self.db_pool.execute("SELECT 1")
                connections["database"] = "connected"
            else:
                connections["database"] = "disconnected"
        except Exception:
            connections["database"] = "error"
        
        try:
            # Verificar Redis
            if self.redis:
                await self.redis.ping()
                connections["redis"] = "connected"
            else:
                connections["redis"] = "disconnected"
        except Exception:
            connections["redis"] = "error"
        
        try:
            # Verificar servicios externos
            if self.http_client:
                # Django API
                response = await self.http_client.get(f"{self.django_api_url}/health/")
                connections["django_api"] = "connected" if response.status_code == 200 else "error"
                
                # Notification Service
                response = await self.http_client.get(f"{self.notification_service_url}/health")
                connections["notification_service"] = "connected" if response.status_code == 200 else "error"
                
                # Telemetry Service
                response = await self.http_client.get(f"{self.telemetry_service_url}/health")
                connections["telemetry_service"] = "connected" if response.status_code == 200 else "error"
            else:
                connections["external_services"] = "disconnected"
        except Exception:
            connections["external_services"] = "error"
        
        return connections
    
    # ============================================================================
    # GESTIÓN DE REGLAS DE ALERTA
    # ============================================================================
    
    async def create_alert_rule(self, rule: AlertRule) -> int:
        """Crear una nueva regla de alerta"""
        try:
            query = """
                INSERT INTO alerts_rule (
                    name, description, module, alert_type, conditions, actions,
                    frequency, status, is_active, priority, cooldown_minutes,
                    created_at, updated_at, created_by
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
                RETURNING id
            """
            
            rule_id = await self.db_pool.fetchval(
                query,
                rule.name,
                rule.description,
                rule.module,
                rule.alert_type,
                json.dumps([c.dict() for c in rule.conditions]),
                json.dumps([a.dict() for a in rule.actions]),
                rule.frequency,
                rule.status,
                rule.is_active,
                rule.priority,
                rule.cooldown_minutes,
                datetime.now(CHILE_TZ),
                datetime.now(CHILE_TZ),
                rule.created_by
            )
            
            logger.info(f"Alert rule created: {rule.name} (ID: {rule_id})")
            return rule_id
            
        except Exception as e:
            logger.error(f"Error creating alert rule: {e}")
            raise
    
    async def get_alert_rules(self, module: Optional[str] = None, 
                            is_active: Optional[bool] = None) -> List[Dict]:
        """Obtener reglas de alerta"""
        try:
            conditions = []
            params = []
            param_count = 0
            
            if module:
                param_count += 1
                conditions.append(f"module = ${param_count}")
                params.append(module)
            
            if is_active is not None:
                param_count += 1
                conditions.append(f"is_active = ${param_count}")
                params.append(is_active)
            
            where_clause = " AND ".join(conditions) if conditions else "1=1"
            
            query = f"""
                SELECT * FROM alerts_rule 
                WHERE {where_clause}
                ORDER BY priority DESC, created_at DESC
            """
            
            rows = await self.db_pool.fetch(query, *params)
            rules = []
            
            for row in rows:
                rule_dict = dict(row)
                # Parsear JSON de condiciones y acciones
                rule_dict['conditions'] = json.loads(rule_dict['conditions'])
                rule_dict['actions'] = json.loads(rule_dict['actions'])
                rules.append(rule_dict)
            
            return rules
            
        except Exception as e:
            logger.error(f"Error getting alert rules: {e}")
            return []
    
    async def get_alert_rule(self, rule_id: int) -> Optional[Dict]:
        """Obtener una regla de alerta específica"""
        try:
            query = "SELECT * FROM alerts_rule WHERE id = $1"
            row = await self.db_pool.fetchrow(query, rule_id)
            
            if row:
                rule_dict = dict(row)
                rule_dict['conditions'] = json.loads(rule_dict['conditions'])
                rule_dict['actions'] = json.loads(rule_dict['actions'])
                return rule_dict
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting alert rule: {e}")
            return None
    
    async def update_alert_rule(self, rule_id: int, rule: AlertRule) -> bool:
        """Actualizar una regla de alerta"""
        try:
            query = """
                UPDATE alerts_rule SET
                    name = $2, description = $3, module = $4, alert_type = $5,
                    conditions = $6, actions = $7, frequency = $8, status = $9,
                    is_active = $10, priority = $11, cooldown_minutes = $12,
                    updated_at = $13
                WHERE id = $1
            """
            
            result = await self.db_pool.execute(
                query,
                rule_id,
                rule.name,
                rule.description,
                rule.module,
                rule.alert_type,
                json.dumps([c.dict() for c in rule.conditions]),
                json.dumps([a.dict() for a in rule.actions]),
                rule.frequency,
                rule.status,
                rule.is_active,
                rule.priority,
                rule.cooldown_minutes,
                datetime.now(CHILE_TZ)
            )
            
            return "UPDATE 1" in result
            
        except Exception as e:
            logger.error(f"Error updating alert rule: {e}")
            return False
    
    async def delete_alert_rule(self, rule_id: int) -> bool:
        """Eliminar una regla de alerta"""
        try:
            query = "DELETE FROM alerts_rule WHERE id = $1"
            result = await self.db_pool.execute(query, rule_id)
            return "DELETE 1" in result
            
        except Exception as e:
            logger.error(f"Error deleting alert rule: {e}")
            return False
    
    async def activate_alert_rule(self, rule_id: int) -> bool:
        """Activar una regla de alerta"""
        try:
            query = """
                UPDATE alerts_rule 
                SET is_active = true, status = 'active', updated_at = $2
                WHERE id = $1
            """
            result = await self.db_pool.execute(query, rule_id, datetime.now(CHILE_TZ))
            return "UPDATE 1" in result
            
        except Exception as e:
            logger.error(f"Error activating alert rule: {e}")
            return False
    
    async def deactivate_alert_rule(self, rule_id: int) -> bool:
        """Desactivar una regla de alerta"""
        try:
            query = """
                UPDATE alerts_rule 
                SET is_active = false, status = 'inactive', updated_at = $2
                WHERE id = $1
            """
            result = await self.db_pool.execute(query, rule_id, datetime.now(CHILE_TZ))
            return "UPDATE 1" in result
            
        except Exception as e:
            logger.error(f"Error deactivating alert rule: {e}")
            return False
    
    # ============================================================================
    # EJECUCIÓN DE ALERTAS
    # ============================================================================
    
    async def execute_alert_rule(self, rule_id: int) -> bool:
        """Ejecutar una regla de alerta específica"""
        try:
            # Obtener regla
            rule = await self.get_alert_rule(rule_id)
            if not rule or not rule['is_active']:
                return False
            
            # Verificar cooldown
            if await self._is_in_cooldown(rule_id, rule['cooldown_minutes']):
                logger.info(f"Rule {rule_id} is in cooldown period")
                return False
            
            # Crear ejecución
            execution_id = await self._create_execution(rule_id)
            
            # Evaluar condiciones
            start_time = datetime.now()
            condition_results = {}
            variable_values = {}
            all_conditions_met = True
            
            for i, condition_data in enumerate(rule['conditions']):
                condition = AlertCondition(**condition_data)
                result = await self._evaluate_condition(condition)
                condition_results[f"condition_{i}"] = result
                
                if not result:
                    all_conditions_met = False
                
                # Obtener valor actual de la variable
                current_value = await self._get_variable_value(condition.variable_name)
                variable_values[condition.variable_name] = current_value
            
            # Calcular duración
            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            
            # Ejecutar acciones si todas las condiciones se cumplen
            action_results = {}
            if all_conditions_met:
                for i, action_data in enumerate(rule['actions']):
                    action = AlertAction(**action_data)
                    result = await self._execute_action(action, rule, variable_values)
                    action_results[f"action_{i}"] = result
            
            # Actualizar ejecución
            await self._update_execution(
                execution_id, 
                ExecutionStatus.SUCCESS if all_conditions_met else ExecutionStatus.NOT_TRIGGERED,
                all_conditions_met,
                duration_ms,
                condition_results,
                action_results,
                variable_values
            )
            
            # Actualizar cooldown si se disparó
            if all_conditions_met:
                await self._set_cooldown(rule_id, rule['cooldown_minutes'])
            
            return all_conditions_met
            
        except Exception as e:
            logger.error(f"Error executing alert rule {rule_id}: {e}")
            await self._update_execution(
                execution_id if 'execution_id' in locals() else None,
                ExecutionStatus.FAILED,
                False,
                0,
                {},
                {},
                {},
                str(e)
            )
            return False
    
    async def execute_all_alert_rules(self):
        """Ejecutar todas las reglas de alerta activas"""
        try:
            rules = await self.get_alert_rules(is_active=True)
            logger.info(f"Executing {len(rules)} active alert rules")
            
            for rule in rules:
                try:
                    await self.execute_alert_rule(rule['id'])
                except Exception as e:
                    logger.error(f"Error executing rule {rule['id']}: {e}")
            
        except Exception as e:
            logger.error(f"Error executing all alert rules: {e}")
    
    async def _evaluate_condition(self, condition: AlertCondition) -> bool:
        """Evaluar una condición específica"""
        try:
            # Obtener valor de la variable
            if condition.function:
                value = await self._get_processed_variable_value(condition)
            else:
                value = await self._get_variable_value(condition.variable_name)
            
            # Aplicar operador
            return self._apply_operator(value, condition.operator, condition.value, condition.secondary_value)
            
        except Exception as e:
            logger.error(f"Error evaluating condition: {e}")
            return False
    
    async def _get_processed_variable_value(self, condition: AlertCondition) -> Any:
        """Obtener valor procesado de la variable con función"""
        try:
            # Obtener historial de la variable
            history = await self._get_variable_history(
                condition.variable_name, 
                condition.time_window or 60
            )
            
            if not history:
                return None
            
            values = [h['value'] for h in history if h['value'] is not None]
            
            if not values:
                return None
            
            # Aplicar función
            if condition.function == ConditionFunction.AVG:
                return statistics.mean(values)
            elif condition.function == ConditionFunction.SUM:
                return sum(values)
            elif condition.function == ConditionFunction.MIN:
                return min(values)
            elif condition.function == ConditionFunction.MAX:
                return max(values)
            elif condition.function == ConditionFunction.COUNT:
                return len(values)
            elif condition.function == ConditionFunction.STD:
                return statistics.stdev(values) if len(values) > 1 else 0
            elif condition.function == ConditionFunction.TREND:
                return self._calculate_trend(values)
            elif condition.function == ConditionFunction.CHANGE:
                return self._calculate_change(values)
            else:
                return values[-1] if values else None
                
        except Exception as e:
            logger.error(f"Error getting processed variable value: {e}")
            return None
    
    def _apply_operator(self, value: Any, operator: ConditionOperator, 
                       target_value: Any, secondary_value: Any = None) -> bool:
        """Aplicar operador de comparación"""
        try:
            if operator == ConditionOperator.EQ:
                return value == target_value
            elif operator == ConditionOperator.NE:
                return value != target_value
            elif operator == ConditionOperator.GT:
                return value > target_value
            elif operator == ConditionOperator.GTE:
                return value >= target_value
            elif operator == ConditionOperator.LT:
                return value < target_value
            elif operator == ConditionOperator.LTE:
                return value <= target_value
            elif operator == ConditionOperator.CONTAINS:
                return target_value in str(value)
            elif operator == ConditionOperator.NOT_CONTAINS:
                return target_value not in str(value)
            elif operator == ConditionOperator.IN:
                return value in target_value if isinstance(target_value, list) else False
            elif operator == ConditionOperator.NOT_IN:
                return value not in target_value if isinstance(target_value, list) else False
            elif operator == ConditionOperator.BETWEEN:
                return target_value <= value <= secondary_value
            elif operator == ConditionOperator.IS_NULL:
                return value is None or value == ""
            elif operator == ConditionOperator.IS_NOT_NULL:
                return value is not None and value != ""
            else:
                return False
                
        except Exception as e:
            logger.error(f"Error applying operator {operator}: {e}")
            return False
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calcular tendencia de valores"""
        if len(values) < 2:
            return "stable"
        
        # Calcular pendiente
        x = list(range(len(values)))
        slope = statistics.linear_regression(x, values).slope
        
        if slope > 0.01:
            return "increasing"
        elif slope < -0.01:
            return "decreasing"
        else:
            return "stable"
    
    def _calculate_change(self, values: List[float]) -> float:
        """Calcular cambio porcentual"""
        if len(values) < 2:
            return 0.0
        
        old_value = values[0]
        new_value = values[-1]
        
        if old_value == 0:
            return 0.0
        
        return ((new_value - old_value) / old_value) * 100
    
    # ============================================================================
    # ACCIONES DE ALERTA
    # ============================================================================
    
    async def _execute_action(self, action: AlertAction, rule: Dict, 
                            variable_values: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecutar una acción de alerta"""
        try:
            if action.action_type == "notification":
                return await self._execute_notification_action(action, rule, variable_values)
            elif action.action_type == "webhook":
                return await self._execute_webhook_action(action, rule, variable_values)
            elif action.action_type == "email":
                return await self._execute_email_action(action, rule, variable_values)
            else:
                logger.warning(f"Unknown action type: {action.action_type}")
                return {"status": "unknown_action_type"}
                
        except Exception as e:
            logger.error(f"Error executing action: {e}")
            return {"status": "error", "error": str(e)}
    
    async def _execute_notification_action(self, action: AlertAction, rule: Dict, 
                                         variable_values: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecutar acción de notificación"""
        try:
            # Preparar datos de contexto
            context_data = {
                "rule_name": rule['name'],
                "alert_type": rule['alert_type'],
                "module": rule['module'],
                "triggered_at": datetime.now(CHILE_TZ).isoformat(),
                **variable_values
            }
            
            # Enviar notificación
            response = await self.http_client.post(
                f"{self.notification_service_url}/notifications/send",
                json={
                    "template_name": action.template_name or "alert_triggered",
                    "module": rule['module'],
                    "user_ids": action.parameters.get("user_ids", []),
                    "context_data": context_data,
                    "priority": "high" if rule['alert_type'] in ['error', 'critical'] else "medium",
                    "related_model": "alerts.rule",
                    "related_id": rule['id']
                }
            )
            
            return {
                "status": "success" if response.status_code == 200 else "error",
                "response": response.json() if response.status_code == 200 else None
            }
            
        except Exception as e:
            logger.error(f"Error executing notification action: {e}")
            return {"status": "error", "error": str(e)}
    
    async def _execute_webhook_action(self, action: AlertAction, rule: Dict, 
                                    variable_values: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecutar acción de webhook"""
        try:
            payload = {
                "rule": rule,
                "variable_values": variable_values,
                "triggered_at": datetime.now(CHILE_TZ).isoformat(),
                **action.parameters
            }
            
            response = await self.http_client.post(
                action.target,
                json=payload,
                headers=action.parameters.get("headers", {})
            )
            
            return {
                "status": "success" if response.status_code < 400 else "error",
                "response_code": response.status_code,
                "response": response.text
            }
            
        except Exception as e:
            logger.error(f"Error executing webhook action: {e}")
            return {"status": "error", "error": str(e)}
    
    async def _execute_email_action(self, action: AlertAction, rule: Dict, 
                                  variable_values: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecutar acción de email"""
        try:
            # Implementar envío de email
            # Por ahora usar notificación como fallback
            return await self._execute_notification_action(action, rule, variable_values)
            
        except Exception as e:
            logger.error(f"Error executing email action: {e}")
            return {"status": "error", "error": str(e)}
    
    # ============================================================================
    # GESTIÓN DE VARIABLES
    # ============================================================================
    
    async def process_variable_data(self, data: VariableData):
        """Procesar datos de variables"""
        try:
            # Guardar en cache
            self.variable_cache[data.variable_name].append(data)
            
            # Limpiar cache antiguo
            cutoff_time = datetime.now(CHILE_TZ) - timedelta(hours=1)
            self.variable_cache[data.variable_name] = [
                v for v in self.variable_cache[data.variable_name]
                if v.timestamp > cutoff_time
            ]
            
            # Guardar en base de datos
            await self._save_variable_data(data)
            
            # Verificar reglas que usan esta variable
            await self._check_variable_rules(data.variable_name)
            
        except Exception as e:
            logger.error(f"Error processing variable data: {e}")
    
    async def _save_variable_data(self, data: VariableData):
        """Guardar datos de variable en base de datos"""
        try:
            query = """
                INSERT INTO alerts_variable_data 
                (variable_name, value, timestamp, source, metadata)
                VALUES ($1, $2, $3, $4, $5)
            """
            
            await self.db_pool.execute(
                query,
                data.variable_name,
                json.dumps(data.value),
                data.timestamp,
                data.source,
                json.dumps(data.metadata)
            )
            
        except Exception as e:
            logger.error(f"Error saving variable data: {e}")
    
    async def _get_variable_value(self, variable_name: str) -> Any:
        """Obtener valor actual de una variable"""
        try:
            # Buscar en cache primero
            if variable_name in self.variable_cache and self.variable_cache[variable_name]:
                return self.variable_cache[variable_name][-1].value
            
            # Buscar en base de datos
            query = """
                SELECT value FROM alerts_variable_data 
                WHERE variable_name = $1 
                ORDER BY timestamp DESC 
                LIMIT 1
            """
            
            row = await self.db_pool.fetchrow(query, variable_name)
            if row:
                return json.loads(row['value'])
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting variable value: {e}")
            return None
    
    async def _get_variable_history(self, variable_name: str, minutes: int) -> List[Dict]:
        """Obtener historial de una variable"""
        try:
            cutoff_time = datetime.now(CHILE_TZ) - timedelta(minutes=minutes)
            
            query = """
                SELECT value, timestamp FROM alerts_variable_data 
                WHERE variable_name = $1 AND timestamp >= $2
                ORDER BY timestamp ASC
            """
            
            rows = await self.db_pool.fetch(query, variable_name, cutoff_time)
            
            return [
                {
                    'value': json.loads(row['value']),
                    'timestamp': row['timestamp']
                }
                for row in rows
            ]
            
        except Exception as e:
            logger.error(f"Error getting variable history: {e}")
            return []
    
    async def _check_variable_rules(self, variable_name: str):
        """Verificar reglas que usan una variable específica"""
        try:
            # Obtener reglas que usan esta variable
            rules = await self.get_alert_rules(is_active=True)
            
            for rule in rules:
                for condition_data in rule['conditions']:
                    if condition_data['variable_name'] == variable_name:
                        # Ejecutar regla
                        await self.execute_alert_rule(rule['id'])
                        break
                        
        except Exception as e:
            logger.error(f"Error checking variable rules: {e}")
    
    # ============================================================================
    # SCHEDULER Y COOLDOWN
    # ============================================================================
    
    async def _scheduler_loop(self):
        """Loop principal del scheduler"""
        while True:
            try:
                # Obtener reglas que necesitan ejecución
                rules = await self._get_rules_to_execute()
                
                for rule in rules:
                    try:
                        await self.execute_alert_rule(rule['id'])
                    except Exception as e:
                        logger.error(f"Error in scheduler for rule {rule['id']}: {e}")
                
                # Esperar antes de la siguiente iteración
                await asyncio.sleep(60)  # Revisar cada minuto
                
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                await asyncio.sleep(60)
    
    async def _get_rules_to_execute(self) -> List[Dict]:
        """Obtener reglas que necesitan ejecución"""
        try:
            rules = await self.get_alert_rules(is_active=True)
            current_time = datetime.now(CHILE_TZ)
            
            rules_to_execute = []
            
            for rule in rules:
                if rule['frequency'] == 'immediate':
                    continue  # Las reglas inmediatas se ejecutan por eventos
                
                next_execution = rule.get('next_execution')
                if not next_execution or current_time >= next_execution:
                    rules_to_execute.append(rule)
            
            return rules_to_execute
            
        except Exception as e:
            logger.error(f"Error getting rules to execute: {e}")
            return []
    
    async def _is_in_cooldown(self, rule_id: int, cooldown_minutes: int) -> bool:
        """Verificar si una regla está en período de cooldown"""
        if cooldown_minutes <= 0:
            return False
        
        try:
            cooldown_key = f"alert_cooldown:{rule_id}"
            cooldown_until = await self.redis.get(cooldown_key)
            
            if cooldown_until:
                cooldown_time = datetime.fromisoformat(cooldown_until.decode())
                return datetime.now(CHILE_TZ) < cooldown_time
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking cooldown: {e}")
            return False
    
    async def _set_cooldown(self, rule_id: int, cooldown_minutes: int):
        """Establecer período de cooldown para una regla"""
        if cooldown_minutes <= 0:
            return
        
        try:
            cooldown_key = f"alert_cooldown:{rule_id}"
            cooldown_until = datetime.now(CHILE_TZ) + timedelta(minutes=cooldown_minutes)
            
            await self.redis.setex(
                cooldown_key,
                cooldown_minutes * 60,
                cooldown_until.isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error setting cooldown: {e}")
    
    # ============================================================================
    # GESTIÓN DE EJECUCIONES
    # ============================================================================
    
    async def _create_execution(self, rule_id: int) -> int:
        """Crear registro de ejecución"""
        try:
            query = """
                INSERT INTO alerts_execution 
                (rule_id, status, execution_time)
                VALUES ($1, $2, $3)
                RETURNING id
            """
            
            execution_id = await self.db_pool.fetchval(
                query,
                rule_id,
                ExecutionStatus.RUNNING,
                datetime.now(CHILE_TZ)
            )
            
            return execution_id
            
        except Exception as e:
            logger.error(f"Error creating execution: {e}")
            return None
    
    async def _update_execution(self, execution_id: int, status: ExecutionStatus, 
                              triggered: bool, duration_ms: int, condition_results: Dict,
                              action_results: Dict, variable_values: Dict, 
                              error_message: Optional[str] = None):
        """Actualizar registro de ejecución"""
        try:
            if not execution_id:
                return
            
            query = """
                UPDATE alerts_execution SET
                    status = $2, triggered = $3, duration_ms = $4,
                    condition_results = $5, action_results = $6, variable_values = $7,
                    error_message = $8
                WHERE id = $1
            """
            
            await self.db_pool.execute(
                query,
                execution_id,
                status,
                triggered,
                duration_ms,
                json.dumps(condition_results),
                json.dumps(action_results),
                json.dumps(variable_values),
                error_message
            )
            
        except Exception as e:
            logger.error(f"Error updating execution: {e}")
    
    async def get_alert_executions(self, rule_id: Optional[int] = None, 
                                 status: Optional[str] = None, limit: int = 50, 
                                 offset: int = 0) -> List[Dict]:
        """Obtener historial de ejecuciones"""
        try:
            conditions = []
            params = []
            param_count = 0
            
            if rule_id:
                param_count += 1
                conditions.append(f"rule_id = ${param_count}")
                params.append(rule_id)
            
            if status:
                param_count += 1
                conditions.append(f"status = ${param_count}")
                params.append(status)
            
            where_clause = " AND ".join(conditions) if conditions else "1=1"
            
            query = f"""
                SELECT * FROM alerts_execution 
                WHERE {where_clause}
                ORDER BY execution_time DESC
                LIMIT ${param_count + 1} OFFSET ${param_count + 2}
            """
            params.extend([limit, offset])
            
            rows = await self.db_pool.fetch(query, *params)
            executions = []
            
            for row in rows:
                execution_dict = dict(row)
                # Parsear JSON
                execution_dict['condition_results'] = json.loads(execution_dict['condition_results'] or '{}')
                execution_dict['action_results'] = json.loads(execution_dict['action_results'] or '{}')
                execution_dict['variable_values'] = json.loads(execution_dict['variable_values'] or '{}')
                executions.append(execution_dict)
            
            return executions
            
        except Exception as e:
            logger.error(f"Error getting alert executions: {e}")
            return []
    
    # ============================================================================
    # MÉTRICAS Y ESTADÍSTICAS
    # ============================================================================
    
    async def get_metrics(self) -> Dict:
        """Obtener métricas del servicio"""
        try:
            # Estadísticas básicas
            total_rules = await self.db_pool.fetchval("SELECT COUNT(*) FROM alerts_rule")
            active_rules = await self.db_pool.fetchval("SELECT COUNT(*) FROM alerts_rule WHERE is_active = true")
            
            # Ejecuciones de hoy
            today = datetime.now(CHILE_TZ).date()
            total_executions_today = await self.db_pool.fetchval(
                "SELECT COUNT(*) FROM alerts_execution WHERE DATE(execution_time) = $1",
                today
            )
            
            triggered_alerts_today = await self.db_pool.fetchval(
                "SELECT COUNT(*) FROM alerts_execution WHERE DATE(execution_time) = $1 AND triggered = true",
                today
            )
            
            # Tiempo promedio de ejecución
            avg_execution_time = await self.db_pool.fetchval(
                "SELECT AVG(duration_ms) FROM alerts_execution WHERE duration_ms IS NOT NULL"
            ) or 0
            
            # Tasa de error
            total_executions = await self.db_pool.fetchval("SELECT COUNT(*) FROM alerts_execution")
            failed_executions = await self.db_pool.fetchval(
                "SELECT COUNT(*) FROM alerts_execution WHERE status = 'failed'"
            )
            error_rate = (failed_executions / total_executions * 100) if total_executions > 0 else 0
            
            return {
                'total_rules': total_rules or 0,
                'active_rules': active_rules or 0,
                'total_executions_today': total_executions_today or 0,
                'triggered_alerts_today': triggered_alerts_today or 0,
                'average_execution_time_ms': float(avg_execution_time),
                'error_rate': error_rate,
                'most_active_variables': [],  # TODO: Implementar
                'top_triggered_rules': []  # TODO: Implementar
            }
            
        except Exception as e:
            logger.error(f"Error getting metrics: {e}")
            return {}
    
    async def get_alert_stats(self, days: int = 7) -> Dict:
        """Obtener estadísticas de alertas"""
        try:
            cutoff_date = datetime.now(CHILE_TZ) - timedelta(days=days)
            
            # Estadísticas básicas
            total_rules = await self.db_pool.fetchval("SELECT COUNT(*) FROM alerts_rule")
            active_rules = await self.db_pool.fetchval("SELECT COUNT(*) FROM alerts_rule WHERE is_active = true")
            
            # Ejecuciones en el período
            total_executions = await self.db_pool.fetchval(
                "SELECT COUNT(*) FROM alerts_execution WHERE execution_time >= $1",
                cutoff_date
            )
            
            successful_executions = await self.db_pool.fetchval(
                "SELECT COUNT(*) FROM alerts_execution WHERE execution_time >= $1 AND status = 'success'",
                cutoff_date
            )
            
            failed_executions = await self.db_pool.fetchval(
                "SELECT COUNT(*) FROM alerts_execution WHERE execution_time >= $1 AND status = 'failed'",
                cutoff_date
            )
            
            triggered_alerts = await self.db_pool.fetchval(
                "SELECT COUNT(*) FROM alerts_execution WHERE execution_time >= $1 AND triggered = true",
                cutoff_date
            )
            
            # Por estado
            executions_by_status = {}
            status_rows = await self.db_pool.fetch(
                "SELECT status, COUNT(*) FROM alerts_execution WHERE execution_time >= $1 GROUP BY status",
                cutoff_date
            )
            for row in status_rows:
                executions_by_status[row['status']] = row['count']
            
            # Por tipo de alerta
            alerts_by_type = {}
            type_rows = await self.db_pool.fetch(
                "SELECT r.alert_type, COUNT(*) FROM alerts_execution e " +
                "JOIN alerts_rule r ON e.rule_id = r.id " +
                "WHERE e.execution_time >= $1 AND e.triggered = true " +
                "GROUP BY r.alert_type",
                cutoff_date
            )
            for row in type_rows:
                alerts_by_type[row['alert_type']] = row['count']
            
            # Por módulo
            alerts_by_module = {}
            module_rows = await self.db_pool.fetch(
                "SELECT r.module, COUNT(*) FROM alerts_execution e " +
                "JOIN alerts_rule r ON e.rule_id = r.id " +
                "WHERE e.execution_time >= $1 AND e.triggered = true " +
                "GROUP BY r.module",
                cutoff_date
            )
            for row in module_rows:
                alerts_by_module[row['module']] = row['count']
            
            return {
                'total_rules': total_rules or 0,
                'active_rules': active_rules or 0,
                'total_executions': total_executions or 0,
                'successful_executions': successful_executions or 0,
                'failed_executions': failed_executions or 0,
                'triggered_alerts': triggered_alerts or 0,
                'executions_by_status': executions_by_status,
                'alerts_by_type': alerts_by_type,
                'alerts_by_module': alerts_by_module
            }
            
        except Exception as e:
            logger.error(f"Error getting alert stats: {e}")
            return {}
    
    async def get_available_variables(self) -> List[Dict]:
        """Obtener variables disponibles"""
        try:
            # Obtener variables únicas de la base de datos
            rows = await self.db_pool.fetch(
                "SELECT DISTINCT variable_name FROM alerts_variable_data ORDER BY variable_name"
            )
            
            variables = []
            for row in rows:
                variable_name = row['variable_name']
                
                # Obtener último valor
                last_value_row = await self.db_pool.fetchrow(
                    "SELECT value, timestamp FROM alerts_variable_data " +
                    "WHERE variable_name = $1 ORDER BY timestamp DESC LIMIT 1",
                    variable_name
                )
                
                variables.append({
                    'name': variable_name,
                    'last_value': json.loads(last_value_row['value']) if last_value_row else None,
                    'last_update': last_value_row['timestamp'].isoformat() if last_value_row else None,
                    'type': 'numeric' if isinstance(json.loads(last_value_row['value']), (int, float)) else 'string'
                })
            
            return variables
            
        except Exception as e:
            logger.error(f"Error getting available variables: {e}")
            return []
    
    async def get_variable_history(self, variable_name: str, hours: int) -> List[Dict]:
        """Obtener historial de una variable"""
        try:
            cutoff_time = datetime.now(CHILE_TZ) - timedelta(hours=hours)
            
            rows = await self.db_pool.fetch(
                "SELECT value, timestamp FROM alerts_variable_data " +
                "WHERE variable_name = $1 AND timestamp >= $2 " +
                "ORDER BY timestamp ASC",
                variable_name, cutoff_time
            )
            
            history = []
            for row in rows:
                history.append({
                    'value': json.loads(row['value']),
                    'timestamp': row['timestamp'].isoformat()
                })
            
            return history
            
        except Exception as e:
            logger.error(f"Error getting variable history: {e}")
            return [] 