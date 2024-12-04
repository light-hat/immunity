"""
Конфигурация URL-адреса для основного проекта.
"""

# from os import environ
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework import permissions

# api_url = environ.get('API_URL')
# api_port = environ.get('API_PORT')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("", include("frontend.urls")),
    # path('api/user/', include('user_api.urls')),
    path("api/agent/", include("agent_api.urls")),
]
