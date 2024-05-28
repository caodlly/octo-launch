from rest_framework import serializers
from apps.accounts.models import VerificationCode
from apps.accounts.serializers import VerificationKeyError
from apps.accounts.serializers import UpdateUserSerializer


class ResetPasswordSerializer(serializers.ModelSerializer):
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
