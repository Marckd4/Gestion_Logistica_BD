from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    path('', views.inicio_pedidos, name='inicio_pedidos'),
    path('crear/', views.crear_nota, name='crear_nota'),
    path('ingresar-producto/<int:nota_id>/', views.ingresar_producto, name='ingresar_producto'),
    path('agregar-detalle/<int:nota_id>/', views.agregar_detalle_nota, name='agregar_detalle_nota'),
    path('editar-detalle/<int:nota_id>/<int:detalle_id>/', views.editar_detalle_nota, name='editar_detalle_nota'),
    path('eliminar-detalle/<int:nota_id>/<int:detalle_id>/', views.eliminar_detalle_nota, name='eliminar_detalle_nota'),
    path('editar-nota/<int:nota_id>/', views.editar_nota, name='editar_nota'),
    path('terminar-pedido/<int:nota_id>/', views.terminar_pedido, name='terminar_pedido'),
    path('status-pedido/', views.status_pedido, name='status_pedido'),
    path('crear-picking/<int:nota_id>/', views.crear_picking, name='crear_picking'),
    path('descargar-picking-pdf/<int:nota_id>/', views.descargar_picking_pdf, name='descargar_picking_pdf'),
    path('ver-nota/<int:nota_id>/', views.ver_nota_venta, name='ver_nota_venta'),
    path('buscar-cliente/', views.buscar_cliente_por_rut, name='buscar_cliente_por_rut'),
    path('buscar-producto/', views.buscar_producto_por_codigo, name='buscar_producto_por_codigo'),
    path('quiebres-stock/', views.listar_quiebres_stock, name='listar_quiebres_stock'),
    path('api/estadisticas-quiebres/', views.obtener_estadisticas_quiebres, name='obtener_estadisticas_quiebres'),
    path('descargar-quiebres-excel/', views.descargar_quiebres_excel, name='descargar_quiebres_excel'),
    
    # Administración de Usuarios y Permisos
    path('admin/usuarios/', admin_views.manage_users, name='manage_users'),
    path('admin/usuarios/<int:user_id>/<str:module>/actualizar/', admin_views.actualizar_permiso, name='actualizar_permiso'),
    path('admin/usuarios/<int:user_id>/<str:module>/eliminar/', admin_views.eliminar_acceso_modulo, name='eliminar_acceso_modulo'),
    path('admin/usuarios/<int:user_id>/agregar-modulo/', admin_views.agregar_acceso_modulo, name='agregar_acceso_modulo'),
    path('admin/usuarios/<int:user_id>/toggle-superuser/', admin_views.toggle_superuser, name='toggle_superuser'),
    path('admin/usuarios/status/', admin_views.status_usuarios, name='status_usuarios'),
    path('admin/usuarios/<int:user_id>/permisos/', admin_views.ver_permisos_usuario, name='ver_permisos_usuario'),
]
