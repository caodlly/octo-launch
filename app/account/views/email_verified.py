from rest_framework import permissions, status
from rest_framework.views import APIView
from app.account.serializers import CodeSerializer
from rest_framework.response import Response
from app.utils.permissions import EmailNotVerified
from app.account.models import VerificationCode
from app.account.tasks import send_verification_email
from app.user.models import User
from drf_spectacular.utils import extend_schema


class SendEmailCodeVerify(APIView):
    """
    API view to send a verification code via email to the user.
    """

    permission_classes = [permissions.IsAuthenticated, EmailNotVerified]

    @extend_schema(
        request=None,
        responses={204: None},
        operation_id="Send verification code via email",
        summary="Send an email verification code to the user",
    )
    def post(self, request, *args, **kwargs):
        """
        Send the verification code via email.

        This endpoint sends a verification code to the user's email address if the user
        has not yet verified their email.
        """
        send_verification_email.delay(self.request.user.email)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmailCodeVerify(APIView):
    """
    API view to verify the email activation code.
    """

    permission_classes = [permissions.IsAuthenticated, EmailNotVerified]
    serializer_class = CodeSerializer

    @extend_schema(
        operation_id="Verify the email activation code",
        summary="Verify the email activation code and activate the user's email",
        request=CodeSerializer,
        responses={204: None},
    )
    def post(self, request, *args, **kwargs):
        """
        Verify the provided email activation code.

        This endpoint verifies the email activation code submitted by the user. If the code is
        correct, the user's email is marked as verified.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data["code"]

        try:
            model = VerificationCode.objects.get(code=code, user=self.request.user)
        except VerificationCode.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(email=self.request.user.email)
        user.email_verified = True
        user.save()
        model.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
