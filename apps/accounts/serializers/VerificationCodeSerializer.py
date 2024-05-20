from rest_framework import serializers
from apps.accounts.models import VerificationCode


class VerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = "__all__"
