from rest_framework import serializers


class SocialSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=255, required=True)
