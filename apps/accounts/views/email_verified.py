from rest_framework import permissions, status, serializers
from rest_framework.generics import GenericAPIView
from apps.accounts.serializers import StatusSerializer
from rest_framework.response import Response
from apps.utils.permissions import EmailNotVerified
from apps.accounts.models import VerificationCode
from apps.accounts.tasks import send_verification_email
from apps.users.models import User
from drf_spectacular.utils import extend_schema


class EmailCodeSerializer(serializers.Serializer):
    code = serializers.CharField(
        required=True,
        max_length=128,
        write_only=True,
    )


class SendEmailCodeVerified(GenericAPIView):
    """
    API view to send a verification code via email to the user.
    """

    permission_classes = [permissions.IsAuthenticated, EmailNotVerified]
    queryset = None
    serializer_class = StatusSerializer

    @extend_schema(
        request=None,
        operation_id="Send verification code via email",
        summary="Send an email verification code to the user",
    )
    def post(self, request, *args, **kwargs):
        """
        Send the verification code via email.

        This endpoint sends a verification code to the user's email address if the user
        has not yet verified their email.
        """
        if not request.user.email_verified:
            send_verification_email.delay(self.request.user.email)
        return Response(
            self.get_serializer({"status": True}).data, status=status.HTTP_200_OK
        )


class EmailCodeVerified(GenericAPIView):
    """
    API view to verify the email activation code.
    """

    permission_classes = [permissions.IsAuthenticated, EmailNotVerified]
    queryset = User.objects.all()
    serializer_class = EmailCodeSerializer

    @extend_schema(
        operation_id="Verify the email activation code",
        summary="Verify the email activation code and activate the user's email",
        request=EmailCodeSerializer,
        responses={204: None},
    )
    def post(self, request, *args, **kwargs):
        """
        Verify the provided email activation code.

        This endpoint verifies the email activation code submitted by the user. If the code is
        correct, the user's email is marked as verified.
        """
        serializer: EmailCodeVerified = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data["code"]

        try:
            model = VerificationCode.objects.get(code=code, user=self.request.user)
        except VerificationCode.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        user = self.queryset.get(email=self.request.user.email)
        user.email_verified = True
        user.save()
        model.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
