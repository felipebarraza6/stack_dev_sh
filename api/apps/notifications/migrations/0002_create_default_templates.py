"""
Crear plantillas de notificación por defecto para todos los módulos del ERP
"""
from django.db import migrations


def create_default_templates(apps, schema_editor):
    """Crear plantillas de notificación por defecto"""
    NotificationTemplate = apps.get_model('notifications', 'NotificationTemplate')
    
    # Plantillas para Banking
    templates = [
        # Banking
        {
            'name': 'transaction_processed',
            'module': 'banking',
            'notification_type': 'both',
            'subject': 'Transacción procesada - {{ transaction_type }}',
            'message_template': '''
Se ha procesado una transacción en la cuenta {{ account.name }}.

Detalles:
- Tipo: {{ transaction_type }}
- Monto: ${{ amount }}
- Fecha: {{ date }}
- Descripción: {{ description }}

Saldo actual: ${{ account.current_balance }}
            ''',
            'available_variables': {
                'transaction': 'Objeto Transaction',
                'account': 'Objeto BankAccount',
                'amount': 'Monto de la transacción',
                'type': 'Tipo de transacción',
                'date': 'Fecha de la transacción',
                'description': 'Descripción de la transacción'
            }
        },
        {
            'name': 'low_balance_alert',
            'module': 'banking',
            'notification_type': 'both',
            'subject': 'ALERTA: Saldo bajo en cuenta {{ account.name }}',
            'message_template': '''
ALERTA DE SALDO BAJO

La cuenta {{ account.name }} tiene un saldo bajo.

Detalles:
- Saldo actual: ${{ current_balance }}
- Saldo mínimo: ${{ minimum_balance }}

Por favor, revise la cuenta y tome las medidas necesarias.
            ''',
            'available_variables': {
                'account': 'Objeto BankAccount',
                'current_balance': 'Saldo actual',
                'minimum_balance': 'Saldo mínimo configurado'
            }
        },
        
        # Payments
        {
            'name': 'payment_received',
            'module': 'payments',
            'notification_type': 'both',
            'subject': 'Pago recibido - Proyecto {{ project.name }}',
            'message_template': '''
Se ha recibido un pago para el proyecto {{ project.name }}.

Detalles del pago:
- Monto: ${{ amount }}
- Método: {{ method }}
- Fecha: {{ date }}
- Referencia: {{ reference }}

Estado: Completado
            ''',
            'available_variables': {
                'payment': 'Objeto Payment',
                'project': 'Objeto Project',
                'amount': 'Monto del pago',
                'method': 'Método de pago',
                'date': 'Fecha del pago',
                'reference': 'Número de referencia'
            }
        },
        {
            'name': 'payment_overdue',
            'module': 'payments',
            'notification_type': 'both',
            'subject': 'PAGO VENCIDO - Proyecto {{ project.name }}',
            'message_template': '''
PAGO VENCIDO

El proyecto {{ project.name }} tiene un pago vencido.

Detalles:
- Cuota: {{ installment }}
- Monto: ${{ amount }}
- Fecha de vencimiento: {{ due_date }}

Por favor, contacte al cliente para coordinar el pago.
            ''',
            'available_variables': {
                'schedule': 'Objeto PaymentSchedule',
                'project': 'Objeto Project',
                'amount': 'Monto de la cuota',
                'due_date': 'Fecha de vencimiento',
                'installment': 'Número de cuota'
            }
        },
        
        # Quotations
        {
            'name': 'quotation_approved',
            'module': 'quotations',
            'notification_type': 'both',
            'subject': 'Cotización aprobada - {{ number }}',
            'message_template': '''
¡Excelente! La cotización {{ number }} ha sido aprobada.

Detalles:
- Proyecto: {{ project.name }}
- Monto total: ${{ amount }}
- Fecha de emisión: {{ issue_date }}

La cotización está lista para ser convertida en proyecto.
            ''',
            'available_variables': {
                'quotation': 'Objeto Quotation',
                'project': 'Objeto Project',
                'amount': 'Monto total',
                'number': 'Número de cotización',
                'issue_date': 'Fecha de emisión'
            }
        },
        {
            'name': 'quotation_expiring',
            'module': 'quotations',
            'notification_type': 'both',
            'subject': 'Cotización por expirar - {{ number }}',
            'message_template': '''
ATENCIÓN: La cotización {{ number }} está por expirar.

Detalles:
- Proyecto: {{ project.name }}
- Válida hasta: {{ valid_until }}

Por favor, contacte al cliente para confirmar la cotización.
            ''',
            'available_variables': {
                'quotation': 'Objeto Quotation',
                'project': 'Objeto Project',
                'valid_until': 'Fecha de validez',
                'number': 'Número de cotización'
            }
        },
        
        # Invoicing
        {
            'name': 'invoice_created',
            'module': 'invoicing',
            'notification_type': 'both',
            'subject': 'Factura creada - {{ number }}',
            'message_template': '''
Se ha creado una nueva factura para el proyecto {{ project.name }}.

Detalles:
- Número: {{ number }}
- Monto total: ${{ amount }}
- Fecha de vencimiento: {{ due_date }}

La factura está lista para ser enviada al cliente.
            ''',
            'available_variables': {
                'invoice': 'Objeto Invoice',
                'project': 'Objeto Project',
                'amount': 'Monto total',
                'number': 'Número de factura',
                'due_date': 'Fecha de vencimiento'
            }
        },
        {
            'name': 'invoice_overdue',
            'module': 'invoicing',
            'notification_type': 'both',
            'subject': 'FACTURA VENCIDA - {{ number }}',
            'message_template': '''
FACTURA VENCIDA

La factura {{ number }} del proyecto {{ project.name }} está vencida.

Detalles:
- Monto pendiente: ${{ amount }}
- Fecha de vencimiento: {{ due_date }}

Por favor, contacte al cliente para coordinar el pago.
            ''',
            'available_variables': {
                'invoice': 'Objeto Invoice',
                'project': 'Objeto Project',
                'amount': 'Monto pendiente',
                'number': 'Número de factura',
                'due_date': 'Fecha de vencimiento'
            }
        },
        
        # Support
        {
            'name': 'ticket_assigned',
            'module': 'support',
            'notification_type': 'both',
            'subject': 'Ticket asignado - {{ title }}',
            'message_template': '''
Se le ha asignado un nuevo ticket de soporte.

Detalles:
- Título: {{ title }}
- Prioridad: {{ priority }}
- Departamento: {{ department }}
- Proyecto: {{ project }}

Por favor, revise el ticket y tome las acciones necesarias.
            ''',
            'available_variables': {
                'ticket': 'Objeto Ticket',
                'title': 'Título del ticket',
                'priority': 'Prioridad del ticket',
                'department': 'Departamento asignado',
                'project': 'Proyecto relacionado'
            }
        },
        {
            'name': 'ticket_status_changed',
            'module': 'support',
            'notification_type': 'both',
            'subject': 'Estado del ticket actualizado - {{ title }}',
            'message_template': '''
El estado del ticket ha sido actualizado.

Detalles:
- Título: {{ title }}
- Estado anterior: {{ old_status }}
- Estado nuevo: {{ new_status }}
- Proyecto: {{ project }}

El ticket ha cambiado de estado.
            ''',
            'available_variables': {
                'ticket': 'Objeto Ticket',
                'title': 'Título del ticket',
                'old_status': 'Estado anterior',
                'new_status': 'Estado nuevo',
                'project': 'Proyecto relacionado'
            }
        },
        
        # Projects
        {
            'name': 'project_created',
            'module': 'projects',
            'notification_type': 'both',
            'subject': 'Nuevo proyecto creado - {{ name }}',
            'message_template': '''
Se ha creado un nuevo proyecto.

Detalles:
- Nombre: {{ name }}
- Cliente: {{ client }}
- Código interno: {{ code }}

El proyecto está listo para comenzar.
            ''',
            'available_variables': {
                'project': 'Objeto Project',
                'client': 'Nombre del cliente',
                'name': 'Nombre del proyecto',
                'code': 'Código interno'
            }
        }
    ]
    
    # Crear plantillas
    for template_data in templates:
        NotificationTemplate.objects.get_or_create(
            name=template_data['name'],
            module=template_data['module'],
            defaults=template_data
        )


def remove_default_templates(apps, schema_editor):
    """Eliminar plantillas de notificación por defecto"""
    NotificationTemplate = apps.get_model('notifications', 'NotificationTemplate')
    template_names = [
        'transaction_processed', 'low_balance_alert',
        'payment_received', 'payment_overdue',
        'quotation_approved', 'quotation_expiring',
        'invoice_created', 'invoice_overdue',
        'ticket_assigned', 'ticket_status_changed',
        'project_created'
    ]
    NotificationTemplate.objects.filter(name__in=template_names).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_templates, remove_default_templates),
    ] 