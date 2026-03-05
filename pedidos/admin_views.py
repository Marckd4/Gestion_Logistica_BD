from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from .models import UserModulePermission, UserConnectionStatus


def is_admin(user):
    """Verificar si el usuario es superuser o staff"""
    return user.is_superuser or user.is_staff


@login_required
@user_passes_test(is_admin)
def manage_users(request):
    """Vista para administrar usuarios y sus permisos"""
    usuarios = User.objects.all().order_by('username')
    modulos = UserModulePermission.MODULE_CHOICES
    
    # Construir estructura de permisos por usuario
    usuarios_data = []
    for usuario in usuarios:
        permisos = UserModulePermission.objects.filter(user=usuario)
        modulos_acceso = {perm.module: perm for perm in permisos}
        
        usuarios_data.append({
            'usuario': usuario,
            'modulos_acceso': modulos_acceso,
            'total_modulos': len(modulos_acceso),
        })
    
    context = {
        'usuarios_data': usuarios_data,
        'modulos': modulos,
        'all_modulos_dict': dict(UserModulePermission.MODULE_CHOICES),
    }
    
    return render(request, 'admin/manage_users.html', context)


@login_required
@user_passes_test(is_admin)
@require_POST
def actualizar_permiso(request, user_id, module):
    """Actualizar un permiso específico de un usuario"""
    usuario = get_object_or_404(User, id=user_id)
    permiso, creado = UserModulePermission.objects.get_or_create(
        user=usuario,
        module=module
    )
    
    # Obtener los permisos a actualizar
    can_view = request.POST.get('can_view') == 'on'
    can_create = request.POST.get('can_create') == 'on'
    can_edit = request.POST.get('can_edit') == 'on'
    can_delete = request.POST.get('can_delete') == 'on'
    can_export = request.POST.get('can_export') == 'on'
    can_report = request.POST.get('can_report') == 'on'
    
    # Actualizar permisos
    permiso.can_view = can_view
    permiso.can_create = can_create
    permiso.can_edit = can_edit
    permiso.can_delete = can_delete
    permiso.can_export = can_export
    permiso.can_report = can_report
    permiso.save()
    
    messages.success(request, f"Permisos de {usuario.username} en {dict(UserModulePermission.MODULE_CHOICES).get(module)} actualizados.")
    return redirect('manage_users')


@login_required
@user_passes_test(is_admin)
@require_POST
def eliminar_acceso_modulo(request, user_id, module):
    """Eliminar acceso completo a un módulo"""
    usuario = get_object_or_404(User, id=user_id)
    
    try:
        permiso = UserModulePermission.objects.get(user=usuario, module=module)
        nombre_modulo = permiso.get_module_display()
        permiso.delete()
        messages.success(request, f"Acceso de {usuario.username} al módulo {nombre_modulo} ha sido eliminado.")
    except UserModulePermission.DoesNotExist:
        messages.warning(request, "Este acceso no existe.")
    
    return redirect('manage_users')


@login_required
@user_passes_test(is_admin)
@require_POST
def agregar_acceso_modulo(request, user_id):
    """Agregar acceso a un módulo para un usuario"""
    usuario = get_object_or_404(User, id=user_id)
    module = request.POST.get('module')
    
    if not module:
        messages.error(request, "Debes seleccionar un módulo.")
        return redirect('manage_users')
    
    # Verificar si ya tiene acceso
    if UserModulePermission.objects.filter(user=usuario, module=module).exists():
        messages.warning(request, f"{usuario.username} ya tiene acceso a este módulo.")
        return redirect('manage_users')
    
    # Crear acceso con permiso de vista por defecto
    permiso = UserModulePermission.objects.create(
        user=usuario,
        module=module,
        can_view=True  # Por defecto, solo puede ver
    )
    
    nombre_modulo = permiso.get_module_display()
    messages.success(request, f"{usuario.username} ahora tiene acceso al módulo {nombre_modulo}.")
    
    return redirect('manage_users')


@login_required
@user_passes_test(is_admin)
def ver_permisos_usuario(request, user_id):
    """Vista detallada de permisos de un usuario (AJAX)"""
    usuario = get_object_or_404(User, id=user_id)
    permisos = UserModulePermission.objects.filter(user=usuario)
    
    datos = {
        'usuario': usuario.username,
        'permisos': []
    }
    
    for perm in permisos:
        datos['permisos'].append({
            'module': perm.module,
            'module_display': perm.get_module_display(),
            'can_view': perm.can_view,
            'can_create': perm.can_create,
            'can_edit': perm.can_edit,
            'can_delete': perm.can_delete,
            'can_export': perm.can_export,
            'can_report': perm.can_report,
        })
    
    return JsonResponse(datos)


@login_required
@require_POST
def toggle_superuser(request, user_id):
    """Activa o desactiva el rol de superusuario para un usuario."""
    if not request.user.is_superuser:
        messages.error(request, "Solo un superusuario puede cambiar este rol.")
        return redirect('manage_users')

    usuario = get_object_or_404(User, id=user_id)

    if usuario == request.user and usuario.is_superuser:
        messages.error(request, "No puedes quitarte a ti mismo el rol de superusuario.")
        return redirect('manage_users')

    if usuario.is_superuser:
        total_superusers = User.objects.filter(is_superuser=True).count()
        if total_superusers <= 1:
            messages.error(request, "No se puede desactivar el último superusuario del sistema.")
            return redirect('manage_users')

    usuario.is_superuser = not usuario.is_superuser
    if usuario.is_superuser:
        usuario.is_staff = True
    usuario.save(update_fields=['is_superuser', 'is_staff'])

    estado = "activado" if usuario.is_superuser else "desactivado"
    messages.success(request, f"Superusuario {estado} para {usuario.username}.")
    return redirect('manage_users')


@login_required
@user_passes_test(is_admin)
def status_usuarios(request):
    """Pantalla de estado de usuarios conectados/desconectados."""
    timeout_minutes = 10
    cutoff = timezone.now() - timedelta(minutes=timeout_minutes)

    users = User.objects.all().order_by('username')
    statuses = {
        status.user_id: status
        for status in UserConnectionStatus.objects.select_related('user').all()
    }

    usuarios_status = []
    for usuario in users:
        status = statuses.get(usuario.id)
        last_seen = status.last_seen if status else usuario.last_login
        conectado = bool(last_seen and last_seen >= cutoff)
        modulo_actual = status.current_module if status and status.current_module else "-"

        usuarios_status.append(
            {
                'usuario': usuario,
                'estado': 'Conectado' if conectado else 'Desconectado',
                'conectado': conectado,
                'modulo_actual': modulo_actual,
                'ultima_conexion': last_seen,
            }
        )

    return render(
        request,
        'admin/status_usuarios.html',
        {
            'usuarios_status': usuarios_status,
            'timeout_minutes': timeout_minutes,
        },
    )
