from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """Izinkan hanya user dengan role 'admin'."""
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'role', '').lower() == 'admin'
        )

class IsStaff(BasePermission):
    """Izinkan hanya user dengan role 'staff'."""
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'role', '').lower() == 'staff'
        )

class IsSupervisor(BasePermission):
    """Izinkan hanya user dengan role 'supervisor'."""
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'role', '').lower() == 'supervisor'
        )

class IsAdminOrStaff(BasePermission):
    """Izinkan hanya user dengan role 'admin' atau 'staff'."""
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'role', '').lower() in ['admin', 'staff']
        )

class IsAdminOrSupervisor(BasePermission):
    """Izinkan hanya user dengan role 'admin' atau 'supervisor'."""
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'role', '').lower() in ['admin', 'supervisor']
        )

class IsStaffOrSupervisor(BasePermission):
    """Izinkan hanya user dengan role 'staff' atau 'supervisor'."""
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'role', '').lower() in ['staff', 'supervisor']
        )

# cara menggunakan 
# from common.permissions import IsAdmin, IsSupervisor, IsAdminOrSupervisor