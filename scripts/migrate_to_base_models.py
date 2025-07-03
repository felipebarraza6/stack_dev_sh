#!/usr/bin/env python3
"""
Script para migrar modelos existentes a usar BaseModel
Este script ayuda a identificar y actualizar modelos que pueden usar los modelos base
"""
import os
import sys
import re
from pathlib import Path

# Agregar el directorio del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def find_models_with_audit_fields():
    """Encuentra modelos que tienen campos de auditoría comunes"""
    
    models_dir = project_root / "api" / "apps"
    audit_fields = ['created_at', 'updated_at', 'is_active']
    
    models_to_update = []
    
    for app_dir in models_dir.iterdir():
        if not app_dir.is_dir() or app_dir.name == 'core':
            continue
            
        models_path = app_dir / "models"
        if not models_path.exists():
            continue
            
        for model_file in models_path.rglob("*.py"):
            if model_file.name == "__init__.py":
                continue
                
            with open(model_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Verificar si tiene campos de auditoría
            has_audit_fields = any(field in content for field in audit_fields)
            
            if has_audit_fields:
                # Extraer nombre de la clase del modelo
                class_match = re.search(r'class\s+(\w+)\(models\.Model\):', content)
                if class_match:
                    model_name = class_match.group(1)
                    models_to_update.append({
                        'file': str(model_file.relative_to(project_root)),
                        'model': model_name,
                        'app': app_dir.name,
                        'audit_fields': [field for field in audit_fields if field in content]
                    })
    
    return models_to_update

def generate_migration_plan(models_to_update):
    """Genera un plan de migración"""
    
    print("=" * 80)
    print("PLAN DE MIGRACIÓN A MODELOS BASE")
    print("=" * 80)
    
    for model_info in models_to_update:
        print(f"\n📁 {model_info['file']}")
        print(f"   Modelo: {model_info['model']}")
        print(f"   App: {model_info['app']}")
        print(f"   Campos de auditoría encontrados: {', '.join(model_info['audit_fields'])}")
        
        # Recomendación
        if 'created_at' in model_info['audit_fields'] and 'updated_at' in model_info['audit_fields']:
            if 'is_active' in model_info['audit_fields']:
                print("   ✅ Recomendación: Usar BaseModel")
            else:
                print("   ✅ Recomendación: Usar BaseModel (agregar is_active)")
        else:
            print("   ⚠️  Recomendación: Revisar manualmente")

def show_usage_examples():
    """Muestra ejemplos de uso"""
    
    print("\n" + "=" * 80)
    print("EJEMPLOS DE USO")
    print("=" * 80)
    
    print("""
# Antes (sin BaseModel):
class MiModelo(models.Model):
    nombre = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

# Después (con BaseModel):
from api.apps.core.models import BaseModel

class MiModelo(BaseModel):
    nombre = models.CharField(max_length=100)
    # created_at, updated_at, is_active heredados de BaseModel

# Para modelos con timestamps específicos:
from api.apps.core.models import TimestampedModel

class MiMedicion(TimestampedModel):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    # timestamp, device_timestamp heredados de TimestampedModel
    # created_at, updated_at, is_active heredados de BaseModel

# Para soft delete:
from api.apps.core.models import SoftDeleteModel

class MiDocumento(SoftDeleteModel):
    titulo = models.CharField(max_length=200)
    # deleted_at, deleted_by heredados de SoftDeleteModel
    # created_at, updated_at, is_active heredados de BaseModel
""")

def main():
    """Función principal"""
    
    print("🔍 Buscando modelos con campos de auditoría...")
    models_to_update = find_models_with_audit_fields()
    
    if not models_to_update:
        print("✅ No se encontraron modelos que necesiten migración.")
        return
    
    generate_migration_plan(models_to_update)
    show_usage_examples()
    
    print(f"\n📊 Resumen:")
    print(f"   Total de modelos encontrados: {len(models_to_update)}")
    print(f"   Apps afectadas: {len(set(m['app'] for m in models_to_update))}")
    
    print(f"\n💡 Próximos pasos:")
    print(f"   1. Revisar cada modelo individualmente")
    print(f"   2. Actualizar imports para incluir BaseModel")
    print(f"   3. Cambiar herencia de models.Model a BaseModel")
    print(f"   4. Eliminar campos duplicados (created_at, updated_at, is_active)")
    print(f"   5. Ejecutar makemigrations y migrate")

if __name__ == "__main__":
    main() 