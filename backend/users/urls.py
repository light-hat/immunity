"""
Маршруты для пользовательской версии REST API.
"""

import uuid
from django.views.decorators.csrf import csrf_exempt


from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.project import ProjectAPIView

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("project/", csrf_exempt(ProjectAPIView.as_view({"get": "get", "post": "post"}))),
    path(
        "project/<int:pk>/",
        csrf_exempt(ProjectAPIView.as_view({"get": "retrieve", "put": "put", "delete": "delete"})),
    ),
    path("project/filter/", csrf_exempt(ProjectAPIView.as_view({"get": "filter"}))),
]
