from apps.users.models import User, username_regex
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
import re
import tools

password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,}$"


class UpdateUserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(required=False,
                                      max_length=128, min_length=5, write_only=True)
    password = serializers.CharField(required=False,
                                     max_length=128, min_length=5, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email',
                  'password', 'password2', 'avatar']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'username': {'required': False},
            'email': {'required': False},
        }

    def validate_password(self, value):
        password = value
        password2 = self.initial_data.get("password2")

        if password != password2:
            raise serializers.ValidationError("Password fields didn't match")

        password_check = re.match(password_pattern, value)
        if password_check is None:
            raise serializers.ValidationError("Password is too weak")

        return make_password(value)

    @staticmethod
    def validate_username(value):
        username_check = re.match(username_regex, value)
        if username_check is None:
            raise serializers.ValidationError("Invalid username format")
        return value

    @staticmethod
    def validate_avatar(value):
        return tools.ReSizeImages(value, 450, 450)
