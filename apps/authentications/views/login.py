from django.contrib.auth import login, logout
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.utils.permissions import LoginPermission
from apps.authentications.serializers import LoginSerializer, UserSerializer
from apps.authentications.throttling import AnonThrottlingLogin


class Login(APIView):
    permission_classes = [LoginPermission]
    throttle_classes = [AnonThrottlingLogin]

    @staticmethod
    @extend_schema(request=LoginSerializer, responses=UserSerializer,
                   operation_id="Login Session")
    def post(request):
        login_serializer = LoginSerializer(
            data=request.data, context={'request': request})

        login_serializer.is_valid(raise_exception=True)

        user = login_serializer.validated_data['user']

        login(request, user)
        user_serializer = UserSerializer(user)

        return Response(user_serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    @extend_schema(operation_id="Logout Session")
    def delete(request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
