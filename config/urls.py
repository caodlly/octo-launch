from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView
from drf_spectacular.views import SpectacularAPIView as SpectacularView
from drf_spectacular.utils import extend_schema

# include apps
urlpatterns = [
    path('', include('apps.urls')),
]


# include docs drf spectacular
class SpectacularAPIView(SpectacularView):

    @extend_schema(exclude=True)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


urlpatterns += [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


# include Admin
urlpatterns += [
    path(f'{settings.ADMIN_URL}/', admin.site.urls),
]


# Local Storage
if settings.DEBUG is True:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
