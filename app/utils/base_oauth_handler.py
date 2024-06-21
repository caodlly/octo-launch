"""base_oauth_handler.py: Contains the BaseOAuthHandler class that is inherited by the provider-specific classes."""

import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from app.utils.generate import generate_code
from config.utils.logging.general import Logger

User = get_user_model()

logger = Logger().get()


class BaseOAuthHandler:
    USER_INFO_URL = None
    EMAIL_FIELD = "email"
    NAME_FIELD = "name"

    def __init__(self, access_token):
        self.access_token = access_token

    def get_user_info(self):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            response = requests.get(self.USER_INFO_URL, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            sanitize_message = Logger().sanitize_message(f"Failed to fetch user info: {str(e)}")
            logger.error(sanitize_message)
        return None

    def get_or_create_user(self, user_info):
        email = user_info.get(self.EMAIL_FIELD, "")
        username = email.split("@")[0] + "_" + generate_code(4)
        name = user_info.get(self.NAME_FIELD, username)
        try:
            user, _ = User.objects.get_or_create(
                email=email, defaults={"username": username, "name": name}
            )
            return user
        except Exception as e:
            sanitize_message = Logger().sanitize_message(f"Error creating or retrieving user: {str(e)}")
            logger.error(sanitize_message)
            return None

    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
