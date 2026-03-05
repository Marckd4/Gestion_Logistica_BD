from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal


# ==========================================
#           PERMISOS DE USUARIO
# ==========================================

class UserModulePermission(models.Model):
    MODULE_CHOICES = (
        ('bodegabsf', 'Bodega BSF'),
        ('bodegacentral', 'Bodega Central'),
        ('pedidos', 'Gestión de Pedidos'),
        ('reportes', 'Reportes'),
        ('admin', 'Panel Administrativo'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_permissions')
    module = models.CharField(max_length=50, choices=MODULE_CHOICES)

    can_view = models.BooleanField(default=False, help_text="Ver/Consultar datos")
    can_create = models.BooleanField(default=False, help_text="Crear nuevos registros")
    can_edit = models.BooleanField(default=False, help_text="Editar registros existentes")
    can_delete = models.BooleanField(default=False, help_text="Eliminar registros")
    can_export = models.BooleanField(default=False, help_text="Exportar datos")
    can_report = models.BooleanField(default=False, help_text="Generar reportes")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'module')
        verbose_name = "Permiso de Módulo de Usuario"
        verbose_name_plural = "Permisos de Módulos de Usuarios"

    def __str__(self):
        return f"{self.user.username} - {self.get_module_display()}"


class UserConnectionStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='connection_status')
    current_module = models.CharField(max_length=120, blank=True, default='')
    current_path = models.CharField(max_length=255, blank=True, default='')
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Estado de Conexión de Usuario"
        verbose_name_plural = "Estados de Conexión de Usuarios"

    def __str__(self):
        return f"{self.user.username} - {self.current_module or 'Sin módulo'}"


# ==========================================
#           NOTA DE VENTA
# ==========================================

class NotaVenta(models.Model):

    BODEGA_CHOICES = (
        ('bsf', 'Bodega BSF'),
        ('central', 'Bodega Central'),
    )

    ESTADO_CHOICES = (
        ('borrador', 'Borrador'),
        ('finalizada', 'Finalizada'),
        ('despachada', 'Despachada'),
    )

    fecha = models.DateTimeField(auto_now_add=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)

    # Datos cliente
    cliente = models.CharField(max_length=200, blank=True, null=True)
    rut_cliente = models.CharField(max_length=20, blank=True, null=True)
    giro = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    
    # Dirección
    direccion = models.CharField(max_length=200, blank=True, null=True)
    comuna = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    
    # Entrega
    lugar_de_entrega = models.CharField(max_length=200, blank=True, null=True)
    fecha_entrega = models.DateField(blank=True, null=True)
    hora_entrega = models.TimeField(blank=True, null=True)
    persona_responsable = models.CharField(max_length=200, blank=True, null=True)
    
    # Pago
    forma_pago = models.CharField(max_length=100, blank=True, null=True)

    tipo_bodega = models.CharField(
        max_length=20,
        choices=BODEGA_CHOICES,
        blank=True,
        null=True
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='borrador'
    )

    # Totales
    neto = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    iva = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    IVA_PORCENTAJE = Decimal("0.19")

    def calcular_totales(self):
        neto = sum(
            (detalle.importe_a_facturar for detalle in self.detalles.all()),
            Decimal("0.00")
        )

        iva = neto * self.IVA_PORCENTAJE
        total = neto + iva

        self.neto = neto
        self.iva = iva
        self.total = total
        self.save(update_fields=["neto", "iva", "total"])

        return neto, iva, total

    def __str__(self):
        return f"Nota {self.id} - {self.get_tipo_bodega_display()}"


# ==========================================
#           DETALLE NOTA
# ==========================================

class DetalleNota(models.Model):

    nota = models.ForeignKey(
        NotaVenta,
        on_delete=models.CASCADE,
        related_name="detalles"
    )

    codigo = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField(max_length=350)
    ean = models.CharField(max_length=50, blank=True, null=True)
    dun = models.CharField(max_length=50, blank=True, null=True)
    formato_venta = models.CharField(max_length=50, blank=True, null=True)

    cantidad_solicitada = models.PositiveIntegerField()
    capacidad_x_caja = models.PositiveIntegerField(blank=True, null=True)

    precio_x_caja = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    precio_unitario = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    importe_a_facturar = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    def save(self, *args, **kwargs):
        if not isinstance(self.precio_x_caja, Decimal):
            self.precio_x_caja = Decimal(str(self.precio_x_caja or "0"))

        if not isinstance(self.precio_unitario, Decimal):
            self.precio_unitario = Decimal(str(self.precio_unitario or "0"))

        if self.precio_unitario <= 0 and self.precio_x_caja > 0:
            self.precio_unitario = self.precio_x_caja

        if self.precio_x_caja <= 0 and self.precio_unitario > 0:
            self.precio_x_caja = self.precio_unitario

        self.importe_a_facturar = self.precio_unitario * Decimal(self.cantidad_solicitada)

        super().save(*args, **kwargs)

        # Recalcular totales automáticamente
        self.nota.calcular_totales()

    def __str__(self):
        return f"{self.descripcion} - {self.cantidad_solicitada} cajas"


# ==========================================
#           QUIEBRE DE STOCK
# ==========================================

class QuiebresStock(models.Model):
    """
    Modelo para registrar productos que tuvieron quiebre de stock
    (cantidad solicitada mayor que la disponible)
    """
    nota = models.ForeignKey(
        NotaVenta,
        on_delete=models.CASCADE,
        related_name="quiebres_stock"
    )
    detalle = models.ForeignKey(
        DetalleNota,
        on_delete=models.CASCADE,
        related_name="quiebres_stock"
    )
    
    codigo = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField(max_length=350)
    
    cantidad_solicitada = models.PositiveIntegerField()
    cantidad_entregada = models.PositiveIntegerField()
    cantidad_faltante = models.PositiveIntegerField()
    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Quiebre de Stock"
        verbose_name_plural = "Quiebres de Stock"
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return f"{self.descripcion} - {self.cantidad_faltante} cajas faltantes"