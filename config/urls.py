from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# include apps
urlpatterns = [
    path('api/', include('apps.urls')),
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
