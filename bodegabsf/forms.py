from . import models
from django.forms import ModelForm

class BsfForm(ModelForm):
    class Meta:
        model = models.Bsf
        fields ='__all__' #Incluye todos los campos del modelo



# eliminar - editar
from django import forms
from .models import Bsf

class BsfForm(forms.ModelForm):
    class Meta:
        model = Bsf
        fields = "__all__"
        


# autocompletado

# class BsfForm(forms.ModelForm):
#     class Meta:
#         model = Bsf
#         fields = "__all__"
#         widgets = {
#             'cod_dun': forms.TextInput(attrs={'id': 'id_cod_dun'}),
#             'cod_ean': forms.HiddenInput(attrs={'id': 'id_cod_ean'}),
#             'cod_sistema': forms.HiddenInput(attrs={'id': 'id_cod_sistema'}),
#             'descripcion': forms.HiddenInput(attrs={'id': 'id_descripcion'}),
#         }

from django import forms

class ImportarExcelForm(forms.Form):
    archivo = forms.FileField(label="Archivo Excel (.xlsx)")
