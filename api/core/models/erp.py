"""
Modelos ERP para SmartHydro
Gestión empresarial completa: cotizaciones, finanzas, operaciones
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from .utils import ModelApi
from .users import User
from .catchment_points import Client, ProjectCatchments, CatchmentPoint


class Quote(ModelApi):
    """
    Cotización para servicios hídricos
    """
    # Información básica
    quote_number = models.CharField(
        max_length=50, unique=True, verbose_name='Número de cotización')
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    
    # Cliente y proyecto
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name='Cliente')
    project = models.ForeignKey(
        ProjectCatchments, on_delete=models.CASCADE, verbose_name='Proyecto')
    
    # Fechas
    issue_date = models.DateField(verbose_name='Fecha de emisión')
    valid_until = models.DateField(verbose_name='Válida hasta')
    delivery_date = models.DateField(null=True, blank=True, verbose_name='Fecha de entrega')
    
    # Estados
    STATUS_CHOICES = [
        ('DRAFT', 'Borrador'),
        ('SENT', 'Enviada'),
        ('REVIEWED', 'Revisada'),
        ('APPROVED', 'Aprobada'),
        ('REJECTED', 'Rechazada'),
        ('EXPIRED', 'Expirada'),
        ('CONVERTED', 'Convertida a orden'),
    ]
    
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='DRAFT', verbose_name='Estado')
    
    # Montos
    subtotal = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name='Subtotal')
    tax_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=19.0, verbose_name='Tasa de impuesto (%)')
    tax_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name='Monto de impuesto')
    total = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name='Total')
    
    # Condiciones
    payment_terms = models.TextField(verbose_name='Condiciones de pago')
    delivery_terms = models.TextField(verbose_name='Condiciones de entrega')
    warranty_terms = models.TextField(verbose_name='Condiciones de garantía')
    
    # Responsable
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Creado por')
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='approved_quotes', verbose_name='Aprobado por')
    
    # Notas
    internal_notes = models.TextField(blank=True, verbose_name='Notas internas')
    client_notes = models.TextField(blank=True, verbose_name='Notas para cliente')
    
    class Meta:
        verbose_name = 'Cotización'
        verbose_name_plural = 'Cotizaciones'
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"Cotización {self.quote_number} - {self.client.name}"
    
    def save(self, *args, **kwargs):
        """Calcular totales automáticamente"""
        if not self.pk:  # Nueva cotización
            self.quote_number = self.generate_quote_number()
        
        self.calculate_totals()
        super().save(*args, **kwargs)
    
    def generate_quote_number(self):
        """Generar número de cotización único"""
        from datetime import datetime
        year = datetime.now().year
        last_quote = Quote.objects.filter(
            quote_number__startswith=f"COT-{year}"
        ).order_by('-quote_number').first()
        
        if last_quote:
            last_number = int(last_quote.quote_number.split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1
        
        return f"COT-{year}-{new_number:04d}"
    
    def calculate_totals(self):
        """Calcular totales de la cotización"""
        self.subtotal = sum(item.total for item in self.items.all())
        self.tax_amount = self.subtotal * (self.tax_rate / Decimal('100'))
        self.total = self.subtotal + self.tax_amount


class QuoteItem(ModelApi):
    """
    Item de cotización
    """
    quote = models.ForeignKey(
        Quote, on_delete=models.CASCADE, related_name='items', verbose_name='Cotización')
    
    # Producto/Servicio
    item_type = models.CharField(max_length=50, verbose_name='Tipo de item')
    description = models.TextField(verbose_name='Descripción')
    specifications = models.JSONField(default=dict, verbose_name='Especificaciones')
    
    # Cantidad y precio
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Cantidad')
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Precio unitario')
    discount_percent = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, verbose_name='Descuento (%)')
    
    # Totales
    subtotal = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Subtotal')
    discount_amount = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Monto de descuento')
    total = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Total')
    
    # Entrega
    delivery_date = models.DateField(null=True, blank=True, verbose_name='Fecha de entrega')
    
    class Meta:
        verbose_name = 'Item de Cotización'
        verbose_name_plural = 'Items de Cotización'
    
    def __str__(self):
        return f"{self.description} - {self.quote.quote_number}"
    
    def save(self, *args, **kwargs):
        """Calcular totales del item"""
        self.calculate_totals()
        super().save(*args, **kwargs)
    
    def calculate_totals(self):
        """Calcular totales del item"""
        self.subtotal = self.quantity * self.unit_price
        self.discount_amount = self.subtotal * (self.discount_percent / Decimal('100'))
        self.total = self.subtotal - self.discount_amount


class Invoice(ModelApi):
    """
    Factura
    """
    # Información básica
    invoice_number = models.CharField(
        max_length=50, unique=True, verbose_name='Número de factura')
    quote = models.ForeignKey(
        Quote, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cotización relacionada')
    
    # Cliente y proyecto
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name='Cliente')
    project = models.ForeignKey(
        ProjectCatchments, on_delete=models.CASCADE, verbose_name='Proyecto')
    
    # Fechas
    issue_date = models.DateField(verbose_name='Fecha de emisión')
    due_date = models.DateField(verbose_name='Fecha de vencimiento')
    payment_date = models.DateField(null=True, blank=True, verbose_name='Fecha de pago')
    
    # Estados
    STATUS_CHOICES = [
        ('DRAFT', 'Borrador'),
        ('SENT', 'Enviada'),
        ('PAID', 'Pagada'),
        ('OVERDUE', 'Vencida'),
        ('CANCELLED', 'Cancelada'),
    ]
    
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='DRAFT', verbose_name='Estado')
    
    # Montos
    subtotal = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name='Subtotal')
    tax_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name='Monto de impuesto')
    total = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name='Total')
    paid_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name='Monto pagado')
    
    # Condiciones
    payment_terms = models.TextField(verbose_name='Condiciones de pago')
    
    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"Factura {self.invoice_number} - {self.client.name}"
    
    def save(self, *args, **kwargs):
        """Calcular totales automáticamente"""
        if not self.pk:  # Nueva factura
            self.invoice_number = self.generate_invoice_number()
        
        self.calculate_totals()
        super().save(*args, **kwargs)
    
    def generate_invoice_number(self):
        """Generar número de factura único"""
        from datetime import datetime
        year = datetime.now().year
        last_invoice = Invoice.objects.filter(
            invoice_number__startswith=f"FAC-{year}"
        ).order_by('-invoice_number').first()
        
        if last_invoice:
            last_number = int(last_invoice.invoice_number.split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1
        
        return f"FAC-{year}-{new_number:04d}"
    
    def calculate_totals(self):
        """Calcular totales de la factura"""
        self.subtotal = sum(item.total for item in self.items.all())
        self.tax_amount = self.subtotal * Decimal('0.19')  # 19% IVA
        self.total = self.subtotal + self.tax_amount


class InvoiceItem(ModelApi):
    """
    Item de factura
    """
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name='items', verbose_name='Factura')
    
    # Producto/Servicio
    description = models.TextField(verbose_name='Descripción')
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Cantidad')
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Precio unitario')
    total = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Total')
    
    class Meta:
        verbose_name = 'Item de Factura'
        verbose_name_plural = 'Items de Factura'
    
    def __str__(self):
        return f"{self.description} - {self.invoice.invoice_number}"
    
    def save(self, *args, **kwargs):
        """Calcular total del item"""
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class Expense(ModelApi):
    """
    Gasto operacional
    """
    # Información básica
    expense_number = models.CharField(
        max_length=50, unique=True, verbose_name='Número de gasto')
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    
    # Proyecto relacionado
    project = models.ForeignKey(
        ProjectCatchments, on_delete=models.CASCADE, verbose_name='Proyecto')
    
    # Categorización
    CATEGORY_CHOICES = [
        ('EQUIPMENT', 'Equipos'),
        ('MAINTENANCE', 'Mantenimiento'),
        ('PERSONNEL', 'Personal'),
        ('TRAVEL', 'Viajes'),
        ('SUPPLIES', 'Insumos'),
        ('SERVICES', 'Servicios'),
        ('OTHER', 'Otros'),
    ]
    
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, verbose_name='Categoría')
    
    # Montos
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Monto')
    tax_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name='Monto de impuesto')
    total = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Total')
    
    # Fechas
    expense_date = models.DateField(verbose_name='Fecha del gasto')
    payment_date = models.DateField(null=True, blank=True, verbose_name='Fecha de pago')
    
    # Estados
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('APPROVED', 'Aprobado'),
        ('PAID', 'Pagado'),
        ('REJECTED', 'Rechazado'),
    ]
    
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name='Estado')
    
    # Responsable
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Creado por')
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='approved_expenses', verbose_name='Aprobado por')
    
    # Documentación
    receipt = models.FileField(
        upload_to='expenses/receipts/', null=True, blank=True, verbose_name='Comprobante')
    
    class Meta:
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'
        ordering = ['-expense_date']
    
    def __str__(self):
        return f"Gasto {self.expense_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        """Calcular totales automáticamente"""
        if not self.pk:  # Nuevo gasto
            self.expense_number = self.generate_expense_number()
        
        self.total = self.amount + self.tax_amount
        super().save(*args, **kwargs)
    
    def generate_expense_number(self):
        """Generar número de gasto único"""
        from datetime import datetime
        year = datetime.now().year
        last_expense = Expense.objects.filter(
            expense_number__startswith=f"GAS-{year}"
        ).order_by('-expense_number').first()
        
        if last_expense:
            last_number = int(last_expense.expense_number.split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1
        
        return f"GAS-{year}-{new_number:04d}"


class Equipment(ModelApi):
    """
    Equipos y dispositivos
    """
    # Información básica
    name = models.CharField(max_length=200, verbose_name='Nombre')
    model = models.CharField(max_length=100, verbose_name='Modelo')
    serial_number = models.CharField(
        max_length=100, unique=True, verbose_name='Número de serie')
    
    # Categorización
    CATEGORY_CHOICES = [
        ('SENSOR', 'Sensor'),
        ('TRANSMITTER', 'Transmisor'),
        ('FLOWMETER', 'Flujómetro'),
        ('PUMP', 'Bomba'),
        ('CONTROLLER', 'Controlador'),
        ('OTHER', 'Otro'),
    ]
    
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, verbose_name='Categoría')
    
    # Ubicación
    project = models.ForeignKey(
        ProjectCatchments, on_delete=models.CASCADE, verbose_name='Proyecto')
    point = models.ForeignKey(
        CatchmentPoint, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Punto de captación')
    
    # Especificaciones
    specifications = models.JSONField(default=dict, verbose_name='Especificaciones')
    
    # Fechas
    purchase_date = models.DateField(verbose_name='Fecha de compra')
    warranty_expiry = models.DateField(verbose_name='Vencimiento de garantía')
    installation_date = models.DateField(null=True, blank=True, verbose_name='Fecha de instalación')
    
    # Estados
    STATUS_CHOICES = [
        ('IN_STOCK', 'En stock'),
        ('INSTALLED', 'Instalado'),
        ('MAINTENANCE', 'En mantenimiento'),
        ('RETIRED', 'Retirado'),
        ('LOST', 'Perdido'),
    ]
    
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='IN_STOCK', verbose_name='Estado')
    
    # Costos
    purchase_cost = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Costo de compra')
    installation_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name='Costo de instalación')
    
    # Proveedor
    supplier = models.CharField(max_length=200, verbose_name='Proveedor')
    supplier_contact = models.CharField(max_length=200, blank=True, verbose_name='Contacto del proveedor')
    
    class Meta:
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.serial_number}"
    
    def is_under_warranty(self):
        """Verificar si está bajo garantía"""
        from datetime import date
        return date.today() <= self.warranty_expiry
    
    def get_total_cost(self):
        """Obtener costo total"""
        return self.purchase_cost + self.installation_cost


class Maintenance(ModelApi):
    """
    Mantenimiento de equipos
    """
    # Información básica
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    
    # Equipo
    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, verbose_name='Equipo')
    
    # Tipos
    MAINTENANCE_TYPES = [
        ('PREVENTIVE', 'Preventivo'),
        ('CORRECTIVE', 'Correctivo'),
        ('PREDICTIVE', 'Predictivo'),
        ('EMERGENCY', 'Emergencia'),
    ]
    
    maintenance_type = models.CharField(
        max_length=20, choices=MAINTENANCE_TYPES, verbose_name='Tipo de mantenimiento')
    
    # Fechas
    scheduled_date = models.DateField(verbose_name='Fecha programada')
    completed_date = models.DateField(null=True, blank=True, verbose_name='Fecha de completado')
    
    # Estados
    STATUS_CHOICES = [
        ('SCHEDULED', 'Programado'),
        ('IN_PROGRESS', 'En progreso'),
        ('COMPLETED', 'Completado'),
        ('CANCELLED', 'Cancelado'),
    ]
    
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='SCHEDULED', verbose_name='Estado')
    
    # Responsable
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Asignado a')
    
    # Costos
    estimated_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name='Costo estimado')
    actual_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name='Costo real')
    
    # Resultados
    findings = models.TextField(blank=True, verbose_name='Hallazgos')
    actions_taken = models.TextField(blank=True, verbose_name='Acciones realizadas')
    next_maintenance_date = models.DateField(null=True, blank=True, verbose_name='Próxima fecha de mantenimiento')
    
    class Meta:
        verbose_name = 'Mantenimiento'
        verbose_name_plural = 'Mantenimientos'
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"{self.title} - {self.equipment.name}"
    
    def is_overdue(self):
        """Verificar si está atrasado"""
        from datetime import date
        return self.status == 'SCHEDULED' and date.today() > self.scheduled_date 