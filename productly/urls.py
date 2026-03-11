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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.urls import reverse_lazy
from . import views
from .views import subir_excel_rebaje


urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('admin/', admin.site.urls),
    path('bodegacentral/', include('bodegacentral.urls')),
    path('bodegabsf/', include('bodegabsf.urls')),
    path('resumen/', views.resumen_unificado, name='resumen_unificado'), # resumen de ambas bodegas
    path("exportar-resumen-excel/", views.exportar_resumen_excel, name="exportar_resumen_excel"), # exportar excel resumen 
    path("crear-usuario/", views.crear_usuario, name="crear_usuario"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('logout/', views.logout_usuario, name='logout'),
    path("login/", views.login_usuario, name="login"),
    path("rebaje-excel/", subir_excel_rebaje, name="rebaje_excel"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
            success_url=reverse_lazy("password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path('pedidos/', include('pedidos.urls')),
    
  
    

    

]
