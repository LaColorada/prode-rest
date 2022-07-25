"""Module imports for permissions.
"""
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    """
    Staff permissions
    """

    def has_permission(self, request, view):
        if request.method == "GET":
            return True

        staff_permission = bool(request.user and request.user.is_staff)
        return staff_permission


class IsForecastUserOrReadOnly(permissions.BasePermission):
    """Base permissions for Forecast class"""

    def has_object_permission(self, request, view, obj):
        """Check if user is object owner to edit comment"""
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.Forecast_player.user == request.user or request.user.is_staff
