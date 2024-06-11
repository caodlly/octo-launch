from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from app.account.throttling import AnonThrottlingLogin
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema


class LoginJwtSerializer(TokenObtainPairSerializer):
    default_error_messages = {"no_active_account": _("Email or password is incorrect.")}


class LoginJWT(TokenObtainPairView):
    throttle_classes = [AnonThrottlingLogin]
    serializer_class = LoginJwtSerializer

    @extend_schema(
        operation_id="Login JWT",
        summary="Obtain JWT tokens",
        description="Log in using email and password to get access and refresh JWT tokens.",
        responses={200: TokenObtainPairSerializer},
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle POST request to login and obtain JWT tokens.
        """
        return super().post(request, *args, **kwargs)


class RefreshJWT(TokenRefreshView):
    @extend_schema(
        operation_id="Refresh JWT",
        summary="Refresh JWT tokens",
        description="Refresh the access token using the refresh token.",
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle POST request to refresh JWT tokens.
        """
        return super().post(request, *args, **kwargs)


class VerifyJWT(TokenVerifyView):
    @extend_schema(
        operation_id="Verify JWT",
        summary="Verify JWT token",
        description="Verify if the provided JWT token is valid.",
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Handle POST request to verify JWT tokens.
        """
        return super().post(request, *args, **kwargs)
