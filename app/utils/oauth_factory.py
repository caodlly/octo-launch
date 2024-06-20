"""oauth_factory.py"""

from .providers_handler import (
    GoogleHandler,
    FacebookHandler,
)


def get_oauth_handler(provider, access_token):
    provider_classes = {
        "google": GoogleHandler,
        "facebook": FacebookHandler,
    }
    handler_class = provider_classes.get(provider)
    if handler_class:
        return handler_class(access_token)
    return None
