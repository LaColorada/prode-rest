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
