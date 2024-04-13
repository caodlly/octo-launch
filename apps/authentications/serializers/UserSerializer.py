from apps.users.models import User
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field


class EmailDetails(serializers.Serializer):
    email = serializers.EmailField(required=False, read_only=True)
    verified = serializers.BooleanField(required=False, read_only=True)


class UserSerializer(serializers.ModelSerializer):
    email_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'first_name', 'last_name', 'email_details',
                  'avatar', 'is_superuser',
                  'date_joined', 'last_login']

    @extend_schema_field(EmailDetails)
    def get_email_details(self, obj):
        return EmailDetails({"email": obj.email, "verified": obj.email_verified}).data


class UserSerializerPublic(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    name = serializers.CharField()
    username = serializers.CharField()
    avatar = serializers.ImageField()


class UserSerializerPrivate(UserSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'name',
                  'first_name', 'last_name', 'email', 'avatar']


class UserStatusAuth(serializers.Serializer):
    status = serializers.BooleanField(required=False, read_only=True)
