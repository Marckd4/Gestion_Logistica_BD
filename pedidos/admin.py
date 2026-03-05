from django.contrib import admin
from .models import NotaVenta, DetalleNota, UserModulePermission, UserConnectionStatus, QuiebresStock

@admin.register(NotaVenta)
class NotaVentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'vendedor', 'fecha', 'estado', 'total')
    list_filter = ('estado', 'fecha', 'tipo_bodega')
    search_fields = ('cliente', 'rut_cliente', 'vendedor__username')
    date_hierarchy = 'fecha'

@admin.register(DetalleNota)
class DetalleNotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nota', 'codigo', 'descripcion', 'cantidad_solicitada')
    search_fields = ('codigo', 'descripcion')
    list_filter = ('nota__fecha',)

@admin.register(UserModulePermission)
class UserModulePermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'can_view', 'can_create', 'can_edit', 'can_delete')
    list_filter = ('module', 'can_view', 'can_create', 'can_edit', 'can_delete')
    search_fields = ('user__username',)

@admin.register(UserConnectionStatus)
class UserConnectionStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_module', 'last_seen')
    list_filter = ('last_seen',)
    search_fields = ('user__username',)

@admin.register(QuiebresStock)
class QuiebresStockAdmin(admin.ModelAdmin):
    list_display = ('id', 'nota', 'codigo', 'descripcion_corta', 'cantidad_solicitada', 'cantidad_entregada', 'cantidad_faltante', 'fecha_registro')
    list_filter = ('fecha_registro', 'nota__fecha')
    search_fields = ('codigo', 'descripcion')
    date_hierarchy = 'fecha_registro'
    readonly_fields = ('fecha_registro',)
    
    def descripcion_corta(self, obj):
        return obj.descripcion[:50] + '...' if len(obj.descripcion) > 50 else obj.descripcion
    descripcion_corta.short_description = 'Descripción'

