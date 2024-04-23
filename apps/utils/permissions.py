from rest_framework.permissions import BasePermission, DjangoModelPermissions

SAFE_METHODS = ("GET",)
SELLER_METHODS = ("POST",)
ADMIN_METHODS = ("POST", "PUT", "DELETE")


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_seller()


class UserVerified(BasePermission):
    def has_permission(self, request, view):
        if request.user.email_verified:
            return True
        if request.user.phone_verified:
            return True
        return False


class EmailNotVerified(BasePermission):
    def has_permission(self, request, view):
        return not request.user.email_verified


class ReadOrAdmin(BasePermission):
    def has_permission(self, request, view):
        print(request.method)
        if request.method in SAFE_METHODS:
            return True
        if request.method in ADMIN_METHODS:
            if request.user.is_authenticated:
                if request.user.is_superuser:
                    return True
        return False


class ReadOrWriteSellerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method in SELLER_METHODS:
            if request.user.is_authenticated:
                if request.user.is_seller() or request.user.is_superuser:
                    return True
        if request.method in ADMIN_METHODS:
            if request.user.is_authenticated:
                if request.user.is_superuser:
                    return True
        return False


class LoginPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            if not request.user.is_authenticated:
                return True
        if request.method == "DELETE":
            if request.user.is_authenticated:
                return True
        return False


class RegisterPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return True
        return False


class MePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            if request.user.is_authenticated:
                return True
        if request.method == "POST":
            return True
        return False


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
