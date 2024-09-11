from rest_framework.permissions import BasePermission

from users.models import User

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        # Verifica se o usuário está autenticado e se o seu role é 'admin'
        return request.user and request.user.is_authenticated and request.user.role == User.ADMIN
