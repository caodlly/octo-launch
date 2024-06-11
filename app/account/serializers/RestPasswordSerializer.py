from rest_framework import serializers
from app.account.models import VerificationCode
from app.account.serializers import VerificationKeyError
from app.account.serializers import UpdateUserSerializer


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, min_length=5, write_only=True, required=True
    )
    password2 = serializers.CharField(
        max_length=128, min_length=5, write_only=True, required=True
    )
    email = serializers.EmailField(write_only=True, required=True)

    class Meta:
        model = VerificationCode
        fields = ["key", "email", "password", "password2"]
        extra_kwargs = {"key": {"required": True}}

    def validate(self, data, *args, **kwargs):
        key = data["key"]
        email = data["email"]

        try:
            model = self.Meta.model.objects.get(key=key, user__email=email)
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
