from . import models
from django.forms import ModelForm

class CentralForm(ModelForm):
    class Meta:
        model = models.Central
        fields ='__all__' #Incluye todos los campos del modelo


# eliminar - editar

from django import forms
from .models import Central   # ← CONFIRMAR nombre del modelo

class CentralForm(forms.ModelForm):
    class Meta:
        model = Central
        fields = "__all__"
        widgets = {
            "categoria": forms.Select(choices=[("IMP", "IMP"), ("NAC", "NAC")]),
            "empresa": forms.Select(choices=[("ChileanTrading", "ChileanTrading"), ("Worlpack", "Worlpack")]),
        }


