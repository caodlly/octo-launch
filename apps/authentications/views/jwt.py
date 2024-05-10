from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView,
)
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from apps.authentications.throttling import AnonThrottlingLogin
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema


class LoginJwtSerializer(TokenObtainSerializer):
    default_error_messages = {"no_active_account": _("Email or password is incorrect.")}


class LoginJWT(TokenObtainPairView):
    throttle_classes = [AnonThrottlingLogin]
    serializer_class = LoginJwtSerializer

    @extend_schema(operation_id="Login JWT")
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class RefreshJWT(TokenRefreshView):
    @extend_schema(operation_id="Refresh JWT")
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class VerifyJWT(TokenVerifyView):
    @extend_schema(operation_id="Verify JWT")
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)
