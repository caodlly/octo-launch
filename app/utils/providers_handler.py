"""providers_handler.py: This module contains the classes that handle the OAuth authentication with the providers."""

from .base_oauth_handler import BaseOAuthHandler


class FacebookHandler(BaseOAuthHandler):
    def __init__(self, access_token):
        super().__init__(access_token)
        self.USER_INFO_URL = self.get_user_info_url()

    def get_user_info_url(self):
        """Dynamically constructs the URL for fetching user information."""
        fields = "name,email"
        return f"https://graph.facebook.com/me?fields={fields}&access_token={self.access_token}"


class GoogleHandler(BaseOAuthHandler):
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
