from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
import re
from app.user.models import User
from .UserSerializer import UserSerializer

password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,}$"


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True, max_length=128, write_only=True)
    password = serializers.CharField(required=True, max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ["id", "name", "username", "email", "password", "password2"]
        extra_kwargs = {
            "email": {"required": True},
        }

    def validate_password(self, value):
        password = value
        password2 = self.initial_data.get("password2")
        if password != password2:
            raise serializers.ValidationError(_("Password fields didn't match"))

        password_check = re.match(password_pattern, value)
        if password_check is None:
            raise serializers.ValidationError(
                _(
                    "The password must be at least 6 characters long and contain at least one uppercase letter, "
                    "one lowercase letter, one digit, and one special character (#?!@$%^&*-)."
                )
            )
        return make_password(value)

    def validate(self, value):
        password2 = value.get("password2")
        if password2:
            del value["password2"]
        return value

    def to_representation(self, instance):
        return UserSerializer(instance).data
