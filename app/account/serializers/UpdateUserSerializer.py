from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
import re
from app.user.models import User

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
        fields = ["id", "name", "username", "email", "password", "password2", "avatar"]
        extra_kwargs = {
            "email": {"required": False},
            "name": {"required": False},
            "username": {"required": False},
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
