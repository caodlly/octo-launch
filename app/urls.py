from django.urls import include, path
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularAPIView as SpectacularView
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("", include("app.account.urls")),
]


# include docs drf spectacular
class SpectacularAPIView(SpectacularView):
    @extend_schema(exclude=True)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


urlpatterns += [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
