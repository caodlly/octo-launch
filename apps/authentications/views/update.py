from drf_spectacular.utils import extend_schema
from rest_framework import permissions, generics
from rest_framework.response import Response
from apps.users.models import User
from apps.authentications.serializers import UpdateUserSerializer, UserSerializer


class UpdateProfile(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request in ['PUT', 'PATCH']:
            return UpdateUserSerializer
        return UserSerializer

    def get_object(self):
        return User.objects.get(id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        serializer = UserSerializer(
            User.objects.get(id=request.user.id))
        return Response(serializer.data)

    @extend_schema(operation_id="Update Profile User", responses=UserSerializer)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
