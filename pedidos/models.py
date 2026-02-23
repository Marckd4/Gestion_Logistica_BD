from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal


# ==========================================
#           NOTA DE VENTA
# ==========================================

class NotaVenta(models.Model):

    BODEGA_CHOICES = (
        ('bsf', 'Bodega BSF'),
        ('central', 'Bodega Central'),
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

        # Asegurar que precio_x_caja siempre sea Decimal
        if not isinstance(self.precio_x_caja, Decimal):
            self.precio_x_caja = Decimal(str(self.precio_x_caja))

        # Convertir capacidad a Decimal de forma segura
        capacidad = Decimal(str(self.capacidad_x_caja)) if self.capacidad_x_caja else Decimal("0")

        # Calcular precio unitario
        if capacidad > 0:
            self.precio_unitario = self.precio_x_caja / capacidad
        else:
            self.precio_unitario = Decimal("0.00")

        # Calcular importe total
        self.importe_a_facturar = (
            self.precio_x_caja * Decimal(self.cantidad_solicitada)
        )

        super().save(*args, **kwargs)

        # Recalcular totales automáticamente
        self.nota.calcular_totales()

    def __str__(self):
        return f"{self.descripcion} - {self.cantidad_solicitada} cajas"