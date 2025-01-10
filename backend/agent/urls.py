"""
Маршруты для агентской версии REST API.
"""

from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import ContextAPIViewset, ConfigAPIViewset, DependencyAPIViewset

# Список маршрутов
urlpatterns = [
    path(
        "context/",
        csrf_exempt(ContextAPIViewset.as_view({"post": "post"})),
    ),
    path(
        "config/",
        csrf_exempt(ConfigAPIViewset.as_view({"post": "post"})),
    ),
    path(
        "dependencies/",
        csrf_exempt(DependencyAPIViewset.as_view({"post": "post"})),
    ),
]
