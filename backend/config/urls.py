"""
URL configuration for config project.
"""

import debug_toolbar
from os import environ

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

ENV = environ.get("DJANGO_ENV")


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
    path("", HealthCheckView.as_view(), name="health-check"),
    path("api/", include("api.urls"), name="api"),
]

if ENV == "dev":
    urlpatterns += [
        path("admin/", admin.site.urls, name="admin"),
    ]
    urlpatterns += static(dev.STATIC_URL, document_root=dev.STATIC_ROOT)
    urlpatterns += static(dev.MEDIA_URL, document_root=dev.MEDIA_ROOT)
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

if ENV != "prod":
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
