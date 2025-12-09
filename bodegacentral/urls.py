from django.urls import path
from . import views



urlpatterns = [
    path('', views.index,name='index'),
    path('formulariocentral', views.formulario_central, name="formulariocentral"),
    path('ajax/obtener-datos-dun/', views.buscar_producto, name='ajax_obtener_datos_dun'),
    path('exportar-excel/', views.exportar_excel, name="exportar_excel_productos"),
    path('editar-central/<int:id>/', views.editar_central, name='editar_central'),
    path('eliminar-central/<int:id>/', views.eliminar_central, name='eliminar_central'),
    path('resumen/', views.resumen_central, name='resumen_central'),
   

    

]
