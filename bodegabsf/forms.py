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
