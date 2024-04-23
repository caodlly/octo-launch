from datetime import timedelta
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.utils.permissions import MePermission
from apps.authentications.serializers import UserSerializer, UserStatusAuth


class Me(APIView):
    permission_classes = [MePermission]

    @staticmethod
    @extend_schema(responses=UserSerializer, operation_id="Me")
    @cache_page(timedelta(minutes=5).seconds, key_prefix="user_me_{user_id}")
    def get(request):
        """
        It fetches the user's personal data
        """
        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data)

    @staticmethod
    @extend_schema(operation_id="Me Status", responses=UserStatusAuth)
    def post(request, *args, **kwargs):
        """
        If you are logged in, it returns True.
        If not, it returns False
        """
        return Response(UserStatusAuth({"status": request.user.is_authenticated}).data)
