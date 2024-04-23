from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
import re
import tools
from django.contrib.auth import get_user_model

User = get_user_model()
password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,}$"


class UpdateUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        required=False, max_length=128, min_length=5, write_only=True
    )
    password = serializers.CharField(
        required=False, max_length=128, min_length=5, write_only=True
    )

    class Meta:
        model = User
        fields = ["id", "name", "email", "password", "password2", "avatar"]
        extra_kwargs = {
            "email": {"required": False},
        }

    def validate_password(self, value):
        password = value
        password2 = self.initial_data.get("password2")

        if password != password2:
            raise serializers.ValidationError(_("Password fields didn't match"))

        password_check = re.match(password_pattern, value)
        if password_check is None:
            raise serializers.ValidationError(_("Password is too weak"))

        return make_password(value)

    @staticmethod
    def validate_avatar(value):
        return tools.ReSizeImages(value, 450, 450)
