from django import forms
from django.forms import inlineformset_factory
from .models import NotaVenta, DetalleNota

FORMAS_PAGO = [
    ('', '-- Seleccione forma de pago --'),
    ('efectivo', 'Efectivo'),
    ('transferencia', 'Transferencia Bancaria'),
    ('cheque', 'Cheque'),
    ('tarjeta_credito', 'Tarjeta de Crédito'),
    ('tarjeta_debito', 'Tarjeta de Débito'),
    ('vale_vista', 'Vale Vista'),
    ('credito_30', 'Crédito 30 días'),
    ('credito_60', 'Crédito 60 días'),
    ('credito_90', 'Crédito 90 días'),
    ('webpay', 'WebPay/POS'),
]


class NotaVentaForm(forms.ModelForm):
    class Meta:
        model = NotaVenta
        fields = [
            'cliente',
            'rut_cliente',
            'giro',
            'telefono',
            'direccion',
            'comuna',
            'ciudad',
            'lugar_de_entrega',
            'fecha_entrega',
            'hora_entrega',
            'persona_responsable',
            'forma_pago',
        ]

        widgets = {
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'rut_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'giro': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'comuna': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'lugar_de_entrega': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_entrega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_entrega': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'persona_responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'forma_pago': forms.Select(choices=FORMAS_PAGO, attrs={'class': 'form-control'}),
        }


class DetalleNotaForm(forms.ModelForm):
    class Meta:
        model = DetalleNota
        fields = [
            'codigo',
            'descripcion',
            'cantidad_solicitada',
            'precio_unitario',
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_solicitada': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
        }


DetalleNotaFormSet = inlineformset_factory(
    NotaVenta,
    DetalleNota,
    form=DetalleNotaForm,
    fields=['codigo', 'descripcion', 'cantidad_solicitada', 'precio_unitario'],
    extra=3,
    can_delete=True,
)
