"""
Маршруты для пользовательской версии REST API.
"""

from django.urls import include, path

from .views import GraphDataView

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("graph/data", GraphDataView.as_view(), name="graph-data"),
]
