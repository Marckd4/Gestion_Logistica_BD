from django.urls import path
from . import views

#/bodegabsf/.....

urlpatterns = [
    path('', views.data,name='data'),
    path('formulario/',views.formulario, name='formulario'),
    path('ajax/buscar_producto/', views.buscar_producto, name='buscar_producto'),
    path('formulario/<int:id>/', views.formulario, name='editar'),
    path('exportar-excel/', views.exportar_excel, name="exportar_excel"), # url de exportar excel
    path('editar/<int:id>/', views.editar_bsf, name='editar_bsf'),
    path('eliminar/<int:id>/', views.eliminar_bsf, name='eliminar_bsf'),
    path('resumen-bsf/', views.resumen_bsf, name='resumen_bsf'),
    path('resumen-pedidos/', views.resumen_pedidos, name='resumen_pedidos'),
    path('resumen-pedidos/excel/', views.resumen_pedidos_excel, name='resumen_pedidos_excel'),
    path('resumen-general-pedidos/',views.resumen_general_pedidos,name='resumen_general_pedidos'),
    path('resumen-general-pedidos/excel/',views.resumen_general_pedidos_excel,name='resumen_general_pedidos_excel'),
    path("importar-excel/", views.importar_excel, name="importar_excel"),
    path("borrar-todo/", views.borrar_todo_bsf, name="borrar_todo_bsf"),
 
   
]
