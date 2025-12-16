# from django.contrib import admin
# from .models import Central # para admin

# # registrar los modelo 

# admin.site.register(Central)

from django.contrib import admin
from .models import Central

@admin.register(Central)
class CentralAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'cod_dun', 'saldo', 'stock_fisico')
    search_fields = ('categoria', 'cod_dun', 'descripcion')  # Búsqueda
    list_filter = ('categoria', 'fecha_inv')  # Filtros laterales
    ordering = ('-fecha_inv',)  # Orden por fecha descendente