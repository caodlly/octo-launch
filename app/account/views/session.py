from django.contrib.auth import login, logout
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app.utils.permissions import LoginPermission
from app.account.serializers import LoginSerializer, UserSerializer
from app.account.throttling import AnonThrottlingLogin


class LoginSession(APIView):
    """
    API view for handling user login and logout sessions.
    """

    permission_classes = [LoginPermission]
    throttle_classes = [AnonThrottlingLogin]
    serializer_class = LoginSerializer

    @extend_schema(
        request=LoginSerializer,
        responses=UserSerializer,
        operation_id="Login Session",
        summary="Log in using session authentication.",
    )
    def post(self, request):
        """
        Log in a user using session-based authentication.

        This endpoint validates user credentials and creates a session for the user.
        If the login is successful, it returns the user's serialized data.
        """
        login_serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        login_serializer.is_valid(raise_exception=True)

        user = login_serializer.validated_data["user"]

        login(request, user)
        user_serializer = UserSerializer(user)

        return Response(user_serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    @extend_schema(
        operation_id="Logout Session",
        summary="Log out and terminate the session.",
        request=None,
        responses=None,
    )
    def delete(request):
        """
        Log out the current user and terminate the session.

        This endpoint logs out the user by invalidating their session.
        It does not require any parameters and returns a 204 No Content status upon success.
        """
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
