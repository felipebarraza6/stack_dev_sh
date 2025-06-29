# Estructura del ERP - SmartHydro

## Descripción General

El módulo ERP (Enterprise Resource Planning) de SmartHydro está organizado en módulos especializados que gestionan diferentes aspectos del negocio, desde la gestión de clientes y proyectos hasta el control financiero completo.

## Estructura de Módulos

### 📁 `api/apps/erp/`

```
erp/
├── __init__.py
├── apps.py
├── urls.py
├── projects/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── invoicing/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── quotations/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── payments/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
└── banking/
    ├── __init__.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    └── urls.py
```

## Módulos Especializados

### 1. 📋 Projects (`projects/`)

**Gestión de clientes y proyectos**

#### Modelos:

- **Client**: Información de clientes (nombre, RUT, dirección, contacto)
- **Project**: Proyectos asociados a clientes con puntos de captación

#### Funcionalidades:

- CRUD de clientes y proyectos
- Relación cliente → proyecto → puntos de captación
- Códigos internos y gestión de proyectos

### 2. 💰 Invoicing (`invoicing/`)

**Facturación y gestión de facturas**

#### Modelos:

- **Invoice**: Facturas emitidas a clientes
- **InvoiceItem**: Items individuales de facturas

#### Funcionalidades:

- Generación de facturas desde cotizaciones
- Cálculo automático de totales y saldos
- Estados de facturación (borrador, enviada, pagada, vencida)
- Relación con términos de pago

### 3. 📝 Quotations (`quotations/`)

**Cotizaciones y gestión de costos**

#### Modelos:

- **CostCenter**: Centros de costos para categorización
- **CostCategory**: Categorías de costos (mano de obra, materiales, etc.)
- **Quotation**: Cotizaciones para proyectos
- **QuotationItem**: Items de cotizaciones con márgenes
- **ProjectCost**: Costos reales de proyectos
- **CostEstimate**: Estimaciones vs costos reales

#### Funcionalidades:

- Gestión completa de cotizaciones
- Control de costos por categorías
- Análisis de varianzas (estimado vs real)
- Cálculo automático de márgenes de ganancia
- Estados de cotización (borrador, enviada, aprobada, convertida)

### 4. 💳 Payments (`payments/`)

**Gestión de pagos y cobranzas**

#### Modelos:

- **PaymentMethod**: Métodos de pago disponibles
- **Payment**: Pagos realizados por clientes
- **PaymentSchedule**: Programación de pagos
- **PaymentTerm**: Términos de pago estándar
- **PaymentReceipt**: Comprobantes de pago
- **PaymentApproval**: Aprobaciones de pagos

#### Funcionalidades:

- Registro y seguimiento de pagos
- Programación de cuotas
- Aprobaciones para métodos que lo requieren
- Comprobantes de pago
- Análisis de cobranzas

### 5. 🏦 Banking (`banking/`)

**Gestión bancaria y flujo de caja**

#### Modelos:

- **Bank**: Bancos disponibles
- **BankAccount**: Cuentas bancarias de la empresa
- **Transaction**: Transacciones bancarias
- **CashFlow**: Flujo de caja por períodos
- **BankReconciliation**: Conciliación bancaria

#### Funcionalidades:

- Gestión de múltiples cuentas bancarias
- Registro de transacciones automático
- Flujo de caja por períodos (diario, semanal, mensual)
- Conciliación bancaria
- Análisis de tendencias financieras

## Relaciones entre Módulos

### Flujo Principal:

```
Client → Project → Quotation → Invoice → Payment → Transaction
```

### Relaciones Clave:

- **Project** → **Quotation** (1:N): Un proyecto puede tener múltiples cotizaciones
- **Quotation** → **Invoice** (1:N): Una cotización puede generar múltiples facturas
- **Invoice** → **Payment** (1:N): Una factura puede tener múltiples pagos
- **Payment** → **Transaction** (1:1): Cada pago se registra como transacción bancaria
- **Project** → **ProjectCost** (1:N): Un proyecto tiene múltiples costos
- **Quotation** → **PaymentSchedule** (1:N): Una cotización puede tener programación de pagos

## URLs y Endpoints

### Rutas Principales:

- `/api/erp/` - Rutas principales del ERP
- `/api/erp/quotations/` - Gestión de cotizaciones
- `/api/erp/payments/` - Gestión de pagos
- `/api/erp/banking/` - Gestión bancaria

### Endpoints Destacados:

#### Quotations:

- `GET /quotations/` - Listar cotizaciones
- `POST /quotations/` - Crear cotización
- `GET /quotations/{id}/` - Detalle de cotización
- `POST /quotations/{id}/convert_to_project/` - Convertir a proyecto
- `GET /quotations/expired/` - Cotizaciones expiradas
- `GET /quotations/expiring_soon/` - Cotizaciones próximas a expirar

#### Payments:

- `GET /payments/` - Listar pagos
- `POST /payments/` - Registrar pago
- `GET /payments/summary/` - Resumen de pagos
- `POST /payments/{id}/approve/` - Aprobar pago
- `GET /payment-schedules/overdue/` - Cuotas vencidas
- `GET /payment-schedules/upcoming/` - Cuotas próximas

#### Banking:

- `GET /accounts/` - Listar cuentas bancarias
- `GET /accounts/balances/` - Balances de todas las cuentas
- `GET /accounts/{id}/transactions/` - Transacciones de cuenta
- `GET /transactions/summary/` - Resumen de transacciones
- `POST /transactions/{id}/process/` - Procesar transacción
- `GET /cash-flows/current_period/` - Flujo de caja actual
- `GET /cash-flows/trends/` - Tendencias del flujo de caja

## Características Técnicas

### Validaciones Automáticas:

- Cálculo automático de totales en facturas y cotizaciones
- Validación de montos de pago vs saldo de factura
- Actualización automática de balances bancarios
- Cálculo de varianzas en costos

### Estados y Workflows:

- Estados de cotización: Borrador → Enviada → Aprobada → Convertida
- Estados de factura: Borrador → Enviada → Pagada/Vencida
- Estados de pago: Pendiente → Procesando → Completado
- Estados de transacción: Pendiente → Procesada

### Reportes y Análisis:

- Resumen de pagos por método y período
- Análisis de varianzas en costos
- Flujo de caja por períodos
- Tendencias financieras
- Conciliación bancaria

## Integración con Otros Módulos

### Common:

- Uso de `BaseModel` para timestamps automáticos
- Modelos compartidos para usuarios

### Telemetry:

- Los proyectos se relacionan con puntos de captación
- Los costos pueden estar asociados a equipos de telemetría

### Support:

- Los proyectos pueden generar tickets de soporte
- Los costos pueden estar relacionados con visitas técnicas

## Próximos Pasos

1. **Implementar migraciones** para todos los nuevos modelos
2. **Crear fixtures** con datos de prueba
3. **Implementar tests** para cada módulo
4. **Crear documentación de API** con Swagger/OpenAPI
5. **Implementar dashboards** para visualización de datos
6. **Integrar con APIs bancarias** para sincronización automática
7. **Implementar notificaciones** para eventos importantes
8. **Crear reportes avanzados** con gráficos y análisis

## Beneficios de esta Estructura

- **Modularidad**: Cada módulo es independiente y escalable
- **Trazabilidad**: Flujo completo desde cotización hasta pago
- **Control Financiero**: Gestión completa de flujo de caja
- **Flexibilidad**: Fácil agregar nuevos tipos de costos o métodos de pago
- **Auditoría**: Historial completo de transacciones
- **Análisis**: Datos estructurados para reportes y análisis
