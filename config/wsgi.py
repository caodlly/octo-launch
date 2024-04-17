from django.core.wsgi import get_wsgi_application
from config.utils.buildenvironment import chanageSettingsBasedOnEnvironment

chanageSettingsBasedOnEnvironment()

application = get_wsgi_application()
