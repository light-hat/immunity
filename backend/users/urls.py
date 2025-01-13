"""
Маршруты для пользовательской версии REST API.
"""

import uuid

from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from .views.context import ContextAPIView
from .views.dataset_label import DatasetAPIView
from .views.project import ProjectAPIView
from .views.vulnerability import VulnerabilityAPIView
from .views.context import ContextAPIView, ContextDetailAPIView

urlpatterns = [
    # path("auth/", include("djoser.urls")),
    # path("auth/", include("djoser.urls.jwt")),
    path(
        "project/", csrf_exempt(ProjectAPIView.as_view({"get": "get", "post": "post"}))
    ),
    path(
        "project/<int:pk>/",
        csrf_exempt(
            ProjectAPIView.as_view(
                {"get": "retrieve", "put": "put", "delete": "delete"}
            )
        ),
    ),
    path("project/filter/", csrf_exempt(ProjectAPIView.as_view({"get": "filter"}))),
    path("project/<int:pk>/config/", csrf_exempt(ProjectAPIView.as_view({"get": "retrieve_config"}))),
    path("project/<int:pk>/libs/", csrf_exempt(ProjectAPIView.as_view({"get": "retrieve_libs"}))),
    path(
        "vulnerability/", csrf_exempt(VulnerabilityAPIView.as_view({"get": "filter"}))
    ),
    path("dataset/", csrf_exempt(DatasetAPIView.as_view({"get": "filter"}))),
    path("dataset/counters/", csrf_exempt(DatasetAPIView.as_view({"get": "retrieve_counters"}))),
    path("dataset/markup/", csrf_exempt(DatasetAPIView.as_view({"post": "post"}))),
    path("context/", csrf_exempt(ContextAPIView.as_view({"get": "filter"}))),
    path("context/<int:pk>/", csrf_exempt(ContextDetailAPIView.as_view({"get": "retrieve"}))),
]
