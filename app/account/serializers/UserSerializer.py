from rest_framework import serializers
from app.user.models import User
from drf_spectacular.utils import extend_schema_field


class EmailDetails(serializers.Serializer):
    value = serializers.EmailField(required=False, read_only=True)
    verified = serializers.BooleanField(required=False, read_only=True)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "username",
            "email",
            "avatar",
            "is_superuser",
            "date_joined",
            "last_login",
            "groups",
        ]
        read_only_fields = fields

    @extend_schema_field(EmailDetails)
    def get_email(self, obj):
        return {"value": obj.email, "verified": obj.email_verified}


class UserSerializerPublic(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    avatar = serializers.ImageField()


class UserSerializerPrivate(UserSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "name", "avatar"]


class StatusSerializer(serializers.Serializer):
    status = serializers.BooleanField(required=False, read_only=True)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
