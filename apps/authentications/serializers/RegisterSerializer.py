from apps.users.models import User, username_regex
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
import re

password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,}$"


class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        required=True, max_length=128, write_only=True)
    password = serializers.CharField(
        required=True, max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email',
                  'password', 'password2']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True},
            'email': {'required': True},
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

    def validate(self, value):
        password2 = value.get("password2")
        if password2:
            del value['password2']
        return value
