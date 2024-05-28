from rest_framework import serializers, status
from apps.accounts.models import VerificationCode
from apps.accounts.serializers import UpdateUserSerializer
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class VerificationCodeError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("The verification code is invalid.")
    default_code = "non_field_errors"


class VerificationKeyError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("The verification key is invalid.")
    default_code = "non_field_errors"


class VerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = "__all__"


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = ["key"]


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = ["code"]


class GetKeySerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    code = serializers.CharField(write_only=True)
    key = KeySerializer(read_only=True)

    class Meta:
        model = VerificationCode
        fields = ["key", "code", "email"]

    def validate(self, data, *args, **kwargs):
        email = data.get("email")
        code = data.get("code")
        try:
            query = self.Meta.model.objects.get(user__email=email, code=code)
            data["key"] = query.key
        except self.Meta.model.DoesNotExist:
            raise VerificationCodeError()
        del data["email"]
        del data["code"]
        return data


class ResetPassword(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=5, write_only=True)
    password2 = serializers.CharField(max_length=128, min_length=5, write_only=True)

    class Meta:
        model = VerificationCode
        fields = ["key", "password", "password2"]

    def validate(self, data, *args, **kwargs):
        key = data["key"]
        try:
            model = self.Meta.model.objects.get(key=key)
            user = model.user
        except self.Meta.model.DoesNotExist:
            raise VerificationKeyError()
        data_update = data
        del data_update["key"]
        serializer = UpdateUserSerializer(user, data=data_update, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        model.delete()
        return data
