from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_pedidos, name='inicio_pedidos'),
    path('crear/', views.crear_nota, name='crear_nota'),
    path('ingresar-producto/<int:nota_id>/', views.ingresar_producto, name='ingresar_producto'),
    path('agregar-detalle/<int:nota_id>/', views.agregar_detalle_nota, name='agregar_detalle_nota'),
    path('editar-nota/<int:nota_id>/', views.editar_nota, name='editar_nota'),
    path('terminar-pedido/<int:nota_id>/', views.terminar_pedido, name='terminar_pedido'),
    path('status-pedido/', views.status_pedido, name='status_pedido'),
    path('crear-picking/<int:nota_id>/', views.crear_picking, name='crear_picking'),
    path('descargar-picking-pdf/<int:nota_id>/', views.descargar_picking_pdf, name='descargar_picking_pdf'),
    path('ver-nota/<int:nota_id>/', views.ver_nota_venta, name='ver_nota_venta'),
    path('buscar-cliente/', views.buscar_cliente_por_rut, name='buscar_cliente_por_rut'),
    path('buscar-producto/', views.buscar_producto_por_codigo, name='buscar_producto_por_codigo'),
]

