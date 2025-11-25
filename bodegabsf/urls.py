from django.urls import path
from . import views

#/bodegabsf/.....

urlpatterns = [
    path('', views.data,name='data'),
    path('formulario',views.formulario, name='formulario'),
    path("exportar-excel/", views.exportar_excel, name="exportar_excel"), # url de exportar excel
    path('editar/<int:id>/', views.editar_bsf, name='editar_bsf'),
    path('eliminar/<int:id>/', views.eliminar_bsf, name='eliminar_bsf'),
]
