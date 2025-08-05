"""
URL configuration for config project.
"""

from os import environ
from django.conf import settings
from config import dev
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from config import dev


class HealthCheckView(APIView):
    """
    Простая проверка работоспособности сервиса
    """

    authentication_classes = []
    permission_classes = []
    renderer_classes = [JSONRenderer]

    def get(self, request):
        return Response(
            {"status": "healthy"},
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
            },
        )


urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("api/", include("api.urls"), name="api"),
    path("communication/", include("communication.urls"), name="communication"),
]

if settings.ENV != "prod":
    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/docs/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
        ),
    ]

if settings.DEBUG:
    urlpatterns += [
        path("admin/", admin.site.urls, name="admin"),
    ]
    urlpatterns += static(dev.STATIC_URL, document_root=dev.STATIC_ROOT)
    urlpatterns += static(dev.MEDIA_URL, document_root=dev.MEDIA_ROOT)

    # Debug toolbar URLs - temporarily disabled
    # try:
    #     import debug_toolbar
    #     urlpatterns = [
    #         path("__debug__/", include(debug_toolbar.urls)),
    #     ] + urlpatterns
    # except ImportError:
    #     pass
