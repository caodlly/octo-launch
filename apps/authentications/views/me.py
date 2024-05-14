from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import generics
from apps.utils.permissions import MePermission
from apps.authentications.serializers import UserSerializer, UserStatusAuth


class Me(generics.GenericAPIView):
    permission_classes = [MePermission]

    def get_serializer(self, *args, **kwargs):
        if self.request.method in "POST":
            return UserStatusAuth()
        if self.request.method in "GET":
            return UserSerializer()

    @extend_schema(operation_id="Me")
    def get(self, request):
        """
        It fetches the user's personal data
        """
        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data)

    @extend_schema(operation_id="Me Status", request=None)
    def post(self, request, *args, **kwargs):
        """
        If you are logged in, it returns True.
        If not, it returns False
        """
        return Response(UserStatusAuth({"status": request.user.is_authenticated}).data)
