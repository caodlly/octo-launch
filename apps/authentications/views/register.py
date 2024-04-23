from drf_spectacular.utils import extend_schema
from rest_framework import status, generics
from rest_framework.response import Response
from apps.utils.permissions import RegisterPermission
from apps.authentications.serializers import RegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class Register(generics.CreateAPIView):
    authentication_classes = []
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [RegisterPermission]

    def create(self, request, *args, **kwargs):
        serializer = super().create(request, *args, **kwargs)
        username = serializer.data["username"]
        user_serializer = UserSerializer(User.objects.get(username=username))
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(operation_id="Register a user account", responses=UserSerializer)
    def post(self, request, *args, **kwargs):
        """
        Creates an account for the user
        """
        return super().post(request, *args, **kwargs)
