from drf_spectacular.utils import extend_schema
from rest_framework import status, generics
from rest_framework.response import Response
from apps.utils.permissions import RegisterPermission
from apps.accounts.serializers import RegisterSerializer, UserSerializer
from apps.users.models import User


class Register(generics.CreateAPIView):
    """
    API view for user registration.
    Allows new users to create an account.
    """

    authentication_classes = []
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [RegisterPermission]

    def create(self, request, *args, **kwargs):
        serializer = super().create(request, *args, **kwargs)
        username = serializer.data["username"]
        user_serializer = UserSerializer(User.objects.get(username=username))
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        operation_id="Register a user account",
        summary="Register a new user account.",
        responses=UserSerializer,
    )
    def post(self, request, *args, **kwargs):
        """
        Register a new user account.
        This endpoint allows a new user to register by providing the required details.
        On successful registration, it returns the newly created user's data.
        """
        return super().post(request, *args, **kwargs)
