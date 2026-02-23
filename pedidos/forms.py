from django import forms
from .models import NotaVenta


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
            'forma_pago': forms.TextInput(attrs={'class': 'form-control'}),
        }
