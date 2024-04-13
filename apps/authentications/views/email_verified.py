from rest_framework import permissions, status, generics
from rest_framework.response import Response
from apps.users.models import User
from apps.utils.permissions import EmailNotVerified
from apps.authentications.models import VerificationCode
from apps.authentications.tasks import send_verification_email


class SendCodeEmailVerified(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, EmailNotVerified]

    def post(self, *args, **kwargs):
        send_verification_email.delay(self.request.user.email)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CodeEmailVerified(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, EmailNotVerified]

    def post(self, *args, **kwargs):
        code = self.request.data.get('code')
        if not code:
            return Response({'code': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            model = VerificationCode.objects.get(
                code=code, user=self.request.user)
        except VerificationCode.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(email=self.request.user.email)
        user.email_verified = True
        user.save()
        model.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
