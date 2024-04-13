from rest_framework import serializers
from apps.authentications.models import VerificationCode


class VerificationCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerificationCode
        fields = '__all__'
