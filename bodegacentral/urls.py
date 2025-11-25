from django.urls import path
from . import views

#/bodegacentral/.....

urlpatterns = [
    path('', views.index,name='index'),
    path('formulariocentral',views.formulario, name='formulariocentral'),
    path("exportar-excel/", views.exportar_excel, name="exportar_excel_productos"),
    path('editar-central/<int:id>/', views.editar_central, name='editar_central'),
    path('eliminar-central/<int:id>/', views.eliminar_central, name='eliminar_central'),

]
