from rest_framework import permissions


class IfUserIsAdmin(permissions.BasePermission):
    message = "Действие разрешено только администратору!"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin or request.user.is_superuser
        return False

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user.is_superuser


class IfUserIsModerator(permissions.BasePermission):
    message = "Действие разрешено только модератору!"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role.is_moderator or request.user.is_superuser
        return False

    def has_object_permission(self, request, view, obj):
        return request.user.role.is_moderator or request.user.is_superuser


class IfUserIsAdministrator(permissions.BasePermission):
    message = "Действие разрешено только администратору!"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin or request.user.is_superuser
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAuthorOrAdminOrModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
            or request.user.is_admin
            or request.user.is_moderator
        )
