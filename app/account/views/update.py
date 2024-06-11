from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from app.account.serializers import UpdateUserSerializer, UserSerializer
from app.user.models import User


class UpdateProfile(UpdateAPIView):
    """
    API view to update user profile data.
    Supports both full update (PUT) and partial update (PATCH).
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request in ["GET"]:
            return UserSerializer
        return UpdateUserSerializer

    def get_object(self):
        return User.objects.get(email=self.request.user.email)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        serializer = UserSerializer(User.objects.get(id=request.user.id))
        return Response(serializer.data)

    @extend_schema(
        operation_id="Update Profile User",
        summary="Full Update of User Profile",
        description="Handle the full update of user data using HTTP PUT method.",
        responses=UserSerializer,
    )
    def put(self, request, *args, **kwargs):
        """
        Handle full update of user data.
        """
        return super().put(request, *args, **kwargs)

    @extend_schema(
        operation_id="Update Some Profile User",
        summary="Partial Update of User Profile",
        description="Handle the partial update of user data using HTTP PATCH method.",
        responses=UserSerializer,
    )
    def patch(self, request, *args, **kwargs):
        """
        Handle partial update of user data.
        """
        return super().put(request, *args, **kwargs)
