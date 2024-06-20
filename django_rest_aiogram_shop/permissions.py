from rest_framework.permissions import BasePermission


class IsBotOrStaff(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser or request.user.groups.filter(name='Bots').exists():
            return True
        return False
