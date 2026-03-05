from django.utils import timezone
from .models import UserConnectionStatus


class UserActivityMiddleware:
    TRACK_INTERVAL_SECONDS = 15

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        try:
            user = getattr(request, "user", None)
            if not user or not user.is_authenticated:
                return response

            now = timezone.now()
            now_epoch = int(now.timestamp())
            last_update_epoch = int(request.session.get("_last_status_update_epoch", 0) or 0)

            should_update = (now_epoch - last_update_epoch) >= self.TRACK_INTERVAL_SECONDS
            if not should_update:
                return response

            current_module = self._resolve_module_label(request.path)

            UserConnectionStatus.objects.update_or_create(
                user=user,
                defaults={
                    "current_module": current_module,
                    "current_path": request.path,
                    "last_seen": now,
                },
            )

            request.session["_last_status_update_epoch"] = now_epoch
            request.session.modified = True
        except Exception:
            return response

        return response

    def _resolve_module_label(self, path):
        if path.startswith("/pedidos"):
            return "Pedidos"
        if path.startswith("/bodegabsf"):
            return "Bodega BSF"
        if path.startswith("/bodegacentral"):
            return "Bodega Central"
        if path.startswith("/dashboard"):
            return "Dashboard"
        if path.startswith("/admin"):
            return "Administración"
        return "Inicio"
