from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


# include apps
urlpatterns = i18n_patterns(
    path("", include("apps.urls")),
    path(f"{settings.ADMIN_URL}/", admin.site.urls),
    prefix_default_language=True,
)

# Local Storage
if settings.DEBUG is True:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
    if "local" in settings.TYPE_STORAGE:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
