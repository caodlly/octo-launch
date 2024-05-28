from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from apps.accounts.serializers import (
    StatusSerializer,
    EmailSerializer,
    GetKeySerializer,
    ResetPassword,
)
from apps.accounts.tasks import send_code_reset_password
from drf_spectacular.utils import extend_schema
from apps.accounts.throttling import AnonThrottlingResetPassword
from apps.utils.permissions import NotAuthenticatedPermission


class SendCodeRestPassword(GenericAPIView):
    """
    API view to send a reset password code via email to the user.
    """

    throttle_classes = [AnonThrottlingResetPassword]
    permission_classes = [NotAuthenticatedPermission]
    queryset = None
    serializer_class = EmailSerializer

    @extend_schema(
        request=EmailSerializer,
        responses=StatusSerializer,
        operation_id="Send Reset Password Code",
        summary="Send a reset password code to the user's email",
    )
    def post(self, *args, **kwargs):
        """
        Send a reset password code via email.
        This endpoint sends a reset password code to the user's email address
        if the email is valid and registered in the system.
        """
        serializer = EmailSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        send_code_reset_password.delay(serializer.data.get("email"))
        return Response(
            StatusSerializer({"status": True}).data, status=status.HTTP_200_OK
        )


class VerifyCodeResetPassowrd(GenericAPIView):
    """
    API view to verify a reset password code sent to the user's email.
    """

    permission_classes = [NotAuthenticatedPermission]
    throttle_classes = [AnonThrottlingResetPassword]
    serializer_class = GetKeySerializer

    @extend_schema(
        operation_id="Verify Reset Password Code",
        summary="Verify a reset password code to the user's email",
    )
    def post(self, *args, **kwargs):
        """
        Verify the reset password code.
        This endpoint verifies the reset password code sent to the user's email
        to ensure it matches the code stored in the system.
        """
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer = serializer.validated_data
        return Response(serializer, status=status.HTTP_200_OK)


class ResetPassowrd(GenericAPIView):
    """
    API view to reset the user's password.
    """

    permission_classes = [NotAuthenticatedPermission]
    throttle_classes = [AnonThrottlingResetPassword]
    serializer_class = ResetPassword

    @extend_schema(
        request=ResetPassword,
        responses={204: None},
        operation_id="Reset Password",
        summary="Reset the user's password",
    )
    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
