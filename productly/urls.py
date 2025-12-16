"""
URL configuration for productly project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('admin/', admin.site.urls),
    path('bodegacentral/', include('bodegacentral.urls')),
    path('bodegabsf/', include('bodegabsf.urls')),
    path('resumen/', views.resumen_unificado, name='resumen_unificado'), # resumen de ambas bodegas
    path("exportar-resumen-excel/", views.exportar_resumen_excel, name="exportar_resumen_excel"), # exportar excel resumen 
    path("crear-usuario/", views.crear_usuario, name="crear_usuario"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path("login/", views.login_usuario, name="login"),
    path('pedidos/', include('pedidos.urls')),
    
  
    

    

]
