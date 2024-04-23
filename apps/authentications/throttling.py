from rest_framework.throttling import AnonRateThrottle
from django.conf import settings


class AnonThrottlingLogin(AnonRateThrottle):
    scope = "LoginThrottling"
    rate = f"{settings.LOGIN_THROTTLING}" + f"/{settings.LOGIN_THROTTLING_IN}"

    def allow_request(self, request, view):
        if request.method == "POST":
            return super().allow_request(request, view)
        return True
