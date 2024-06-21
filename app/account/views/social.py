"""oauth_factory.py: Factory function to return the appropriate OAuth handler based on the provider."""

from rest_framework.views import APIView
from rest_framework.response import Response
from config.utils.logging.general import Logger
from django.contrib.auth import get_user_model
from rest_framework import status
from app.utils.oauth_factory import get_oauth_handler

User = get_user_model()
logger = Logger().get()


class OAuthLoginView(APIView):
    """
    Handle Google login, validate access token, register/login user, and return JWT.
    """

    permission_classes = []

    def post(self, request, provider, *args, **kwargs):
        access_token = self.extract_token(request)
        if not access_token:
            return Response(
                {"error": "Access token not provided or improperly formatted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        handler = get_oauth_handler(provider, access_token)
        if not handler:
            return Response(
                {"error": "Unsupported provider."}, status=status.HTTP_400_BAD_REQUEST
            )

        user_info = handler.get_user_info()
        if not user_info:
            return Response(
                {"error": f"Invalid or expired {provider} access token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = handler.get_or_create_user(user_info)
        if not user:
            return Response(
                {"error": "User could not be created or retrieved."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        tokens = handler.get_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_200_OK)

    @staticmethod
    def extract_token(request):
        """Extracts the bearer token from the Authorization header."""
        auth_header = request.headers.get("Authorization", "")
        if "Bearer " in auth_header:
            return auth_header.split("Bearer ")[1].strip()
        else:
            sanitize_message = Logger().sanitize_message(f"Authorization header malformed or missing: {auth_header}")
            logger.error(sanitize_message)
            return auth_header
