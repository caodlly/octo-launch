from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from app.account.serializers.SocialSerializer import SocialSerializer
from octo.handler.social import OAuthGoogle


def get_oauth_handler(provider, access_token):
    provider_classes = {
        "google": OAuthGoogle,
    }
    handler_class = provider_classes.get(provider)
    if handler_class:
        return handler_class(access_token)
    return None


class OAuthLoginView(GenericAPIView):
    """
    Handle Google login, validate access token, register/login user, and return JWT.
    """

    serializer_class = SocialSerializer
    permission_classes = []

    def post(self, request, provider, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.data.get("access_token")

        handler = get_oauth_handler(provider, access_token)
        if not handler:
            ...
        token = handler.generate("jwt")
        print(token)
        if not token:
            ...
        return Response(token, status=status.HTTP_200_OK)
