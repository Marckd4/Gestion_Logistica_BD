from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_nota, name='crear_nota'),
    path('agregar/<int:nota_id>/', views.agregar_producto, name='agregar_producto'),
    path('lista/', views.lista_notas, name='lista_notas'),
    path('detalle/<int:nota_id>/', views.detalle_nota, name='detalle_nota'),
]

