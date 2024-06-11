from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from app.utils.permissions import NotAuthenticatedPermission
from app.account.serializers import RegisterSerializer, UserSerializer
from app.user.models import User


class Register(CreateAPIView):
    """
    API view for user registration.
    Allows new users to create an account.
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [NotAuthenticatedPermission]

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
