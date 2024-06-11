from rest_framework.permissions import BasePermission, DjangoModelPermissions


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class UserVerified(BasePermission):
    def has_permission(self, request, view):
        if request.user.email_verified and request.user.is_staff:
            return True
        return False


class EmailNotVerified(BasePermission):
    def has_permission(self, request, view):
        return not request.user.email_verified


class ReadOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET"]:
            return True
        if request.method in ["POST", "PUT", "DELETE"]:
            if request.user.is_authenticated and request.user.is_superuser:
                return True
        return False


class LoginPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["DELETE"]:
            if not request.user.is_authenticated:
                return False
        return True


class NotAuthenticatedPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return True
        return False


class MePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET"] and not request.user.is_authenticated:
            return False
        return True


class ModelPermissions(DjangoModelPermissions):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }
