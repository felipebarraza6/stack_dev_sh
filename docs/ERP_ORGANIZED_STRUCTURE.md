# Estructura Organizada del ERP - SmartHydro

## Descripción General

El módulo ERP de SmartHydro ha sido reorganizado con una estructura modular y escalable, donde cada módulo tiene sus propios archivos organizados por tipo (models, serializers, views, etc.).

## Nueva Estructura de Carpetas

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
│   ├── urls.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── cost_management.py
│   │   └── quotations.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── cost_management.py
│   │   └── quotations.py
│   └── views/
│       ├── __init__.py
│       ├── cost_management.py
│       └── quotations.py
├── payments/
│   ├── __init__.py
│   ├── urls.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── payment_methods.py
│   │   ├── payments.py
│   │   └── receipts.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── payment_methods.py
│   │   ├── payments.py
│   │   └── receipts.py
│   └── views/
│       ├── __init__.py
│       ├── payment_methods.py
│       ├── payments.py
│       └── receipts.py
└── banking/
    ├── __init__.py
    ├── urls.py
    ├── models/
    │   ├── __init__.py
    │   ├── banks.py
    │   ├── transactions.py
    │   └── cash_flow.py
    ├── serializers/
    │   ├── __init__.py
    │   ├── banks.py
    │   ├── transactions.py
    │   └── cash_flow.py
    └── views/
        ├── __init__.py
        ├── banks.py
        ├── transactions.py
        └── cash_flow.py
```

## Organización por Módulos

### 1. 📋 Projects (Estructura Simple)

**Gestión de clientes y proyectos**

```
projects/
├── models.py          # Client, Project
├── serializers.py     # ClientSerializer, ProjectSerializer
├── views.py          # ClientViewSet, ProjectViewSet
└── urls.py           # URLs del módulo
```

### 2. 💰 Invoicing (Estructura Simple)

**Facturación y gestión de facturas**

```
invoicing/
├── models.py          # Invoice, InvoiceItem
├── serializers.py     # InvoiceSerializer, InvoiceItemSerializer
├── views.py          # InvoiceViewSet, InvoiceItemViewSet
└── urls.py           # URLs del módulo
```

### 3. 📝 Quotations (Estructura Organizada)

**Cotizaciones y gestión de costos**

#### Models:

- `cost_management.py`: CostCenter, CostCategory, ProjectCost, CostEstimate
- `quotations.py`: Quotation, QuotationItem

#### Serializers:

- `cost_management.py`: Serializers para gestión de costos
- `quotations.py`: Serializers para cotizaciones

#### Views:

- `cost_management.py`: ViewSets para gestión de costos
- `quotations.py`: ViewSets para cotizaciones

### 4. 💳 Payments (Estructura Organizada)

**Gestión de pagos y cobranzas**

#### Models:

- `payment_methods.py`: PaymentMethod, PaymentTerm
- `payments.py`: Payment, PaymentSchedule
- `receipts.py`: PaymentReceipt, PaymentApproval

#### Serializers:

- `payment_methods.py`: Serializers para métodos de pago
- `payments.py`: Serializers para pagos
- `receipts.py`: Serializers para comprobantes

#### Views:

- `payment_methods.py`: ViewSets para métodos de pago
- `payments.py`: ViewSets para pagos
- `receipts.py`: ViewSets para comprobantes

### 5. 🏦 Banking (Estructura Organizada)

**Gestión bancaria y flujo de caja**

#### Models:

- `banks.py`: Bank, BankAccount
- `transactions.py`: Transaction
- `cash_flow.py`: CashFlow, BankReconciliation

#### Serializers:

- `banks.py`: Serializers para bancos y cuentas
- `transactions.py`: Serializers para transacciones
- `cash_flow.py`: Serializers para flujo de caja

#### Views:

- `banks.py`: ViewSets para bancos y cuentas
- `transactions.py`: ViewSets para transacciones
- `cash_flow.py`: ViewSets para flujo de caja

## Archivos **init**.py

Cada carpeta tiene su archivo `__init__.py` que importa y expone los modelos, serializers y views:

### Ejemplo para Models:

```python
# quotations/models/__init__.py
from .cost_management import CostCenter, CostCategory, ProjectCost, CostEstimate
from .quotations import Quotation, QuotationItem

__all__ = [
    'CostCenter',
    'CostCategory',
    'Quotation',
    'QuotationItem',
    'ProjectCost',
    'CostEstimate'
]
```

### Ejemplo para Serializers:

```python
# quotations/serializers/__init__.py
from .cost_management import (
    CostCenterSerializer, CostCategorySerializer,
    ProjectCostSerializer, CostEstimateSerializer
)
from .quotations import (
    QuotationSerializer, QuotationItemSerializer,
    QuotationDetailSerializer, QuotationCreateSerializer
)
```

### Ejemplo para Views:

```python
# quotations/views/__init__.py
from .cost_management import (
    CostCenterViewSet, CostCategoryViewSet,
    ProjectCostViewSet, CostEstimateViewSet
)
from .quotations import (
    QuotationViewSet, QuotationItemViewSet
)
```

## Beneficios de esta Organización

### ✅ **Escalabilidad**

- Fácil agregar nuevos modelos sin afectar archivos existentes
- Separación clara de responsabilidades
- Estructura predecible para nuevos desarrolladores

### ✅ **Mantenibilidad**

- Archivos más pequeños y enfocados
- Fácil localizar código específico
- Reducción de conflictos en merge

### ✅ **Reutilización**

- Importaciones específicas por funcionalidad
- Evita importaciones circulares
- Mejor organización de dependencias

### ✅ **Testing**

- Tests más específicos por funcionalidad
- Fácil mockear dependencias
- Mejor cobertura de código

## Convenciones de Nomenclatura

### Archivos de Modelos:

- `cost_management.py` - Gestión de costos
- `quotations.py` - Cotizaciones
- `payment_methods.py` - Métodos de pago
- `payments.py` - Pagos
- `receipts.py` - Comprobantes
- `banks.py` - Bancos y cuentas
- `transactions.py` - Transacciones
- `cash_flow.py` - Flujo de caja

### Archivos de Serializers:

- Mismo nombre que los archivos de modelos
- Sufijo `Serializer` para las clases
- Agrupación lógica por funcionalidad

### Archivos de Views:

- Mismo nombre que los archivos de modelos
- Sufijo `ViewSet` para las clases
- Agrupación por funcionalidad relacionada

## URLs y Routing

### URLs Principales:

```python
# api/apps/erp/urls.py
urlpatterns = [
    path('', include(router.urls)),
    path('quotations/', include('api.apps.erp.quotations.urls')),
    path('payments/', include('api.apps.erp.payments.urls')),
    path('banking/', include('api.apps.erp.banking.urls')),
]
```

### URLs por Módulo:

```python
# quotations/urls.py
router = DefaultRouter()
router.register(r'cost-centers', CostCenterViewSet)
router.register(r'cost-categories', CostCategoryViewSet)
router.register(r'quotations', QuotationViewSet)
router.register(r'quotation-items', QuotationItemViewSet)
router.register(r'project-costs', ProjectCostViewSet)
router.register(r'cost-estimates', CostEstimateViewSet)
```

## Próximos Pasos

1. **Completar la reorganización** de todos los módulos
2. **Crear serializers y views** para los módulos faltantes
3. **Implementar tests** para cada módulo organizado
4. **Crear migraciones** para todos los modelos
5. **Documentar APIs** con Swagger/OpenAPI
6. **Implementar validaciones** específicas por módulo
7. **Crear fixtures** de datos de prueba
8. **Implementar permisos** por módulo

## Migración desde Estructura Anterior

### Antes:

```python
# quotations/models.py (archivo único)
class CostCenter(models.Model):
    # ...

class Quotation(models.Model):
    # ...
```

### Después:

```python
# quotations/models/cost_management.py
class CostCenter(models.Model):
    # ...

# quotations/models/quotations.py
class Quotation(models.Model):
    # ...

# quotations/models/__init__.py
from .cost_management import CostCenter
from .quotations import Quotation
```

Esta estructura organizada hace que el código sea más mantenible, escalable y fácil de entender para todo el equipo de desarrollo.
