from django.core.asgi import get_asgi_application
from config.utils.buildenvironment import chanageSettingsBasedOnEnvironment

chanageSettingsBasedOnEnvironment()

application = get_asgi_application()
