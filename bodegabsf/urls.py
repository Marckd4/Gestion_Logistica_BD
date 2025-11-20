from django.urls import path
from . import views

#/bodegabsf/.....

urlpatterns = [
    path('', views.data,name='data')
]
