from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError, APIException
from django.contrib.auth import authenticate


class AuthenticationFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'No active account found with the given credentials'
    default_code = 'no_active_account'


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=128)
    password = serializers.CharField(
        trim_whitespace=False,
        label="Password",
        style={'input_type': 'password'},
        max_length=128,
        write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        request = self.context.get('request')
        if email and password:
            user = authenticate(
                request=request, email=email, password=password)

            if not user:
                raise AuthenticationFailed()
        else:
            msg = 'Must include "username" and "password".'
            raise ValidationError(msg, code='authorization')
        data['user'] = user
        return data
