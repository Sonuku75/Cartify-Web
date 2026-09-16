"""
Security permission classes for Cartify REST APIs.
Provides standard, reusable authorization boundaries across domains.
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS, AllowAny


class PublicEndpoint(AllowAny):
    """Explicit permission marking endpoints intended for public unauthenticated access."""
    pass


class IsAdminOrReadOnly(BasePermission):
    """
    Allows read-only access to any request, but requires staff/admin status for modifications.
    Ideal for product catalogs, categories, and public marketing content.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsStaffUser(BasePermission):
    """
    Requires the user to be authenticated and have staff status.
    Ideal for internal management, inventory adjustments, and operational endpoints.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit or delete it.
    Assumes the model instance has a `user` or `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        # Check common owner attribute patterns
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if obj == request.user:
            return True

        return False
