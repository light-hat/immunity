"""
Маршруты для агентской версии REST API.
"""

from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import ContextAPIViewset

# Список маршрутов
urlpatterns = [
    path(
        "context/",
        csrf_exempt(ContextAPIViewset.as_view({"post": "post"})),
        name="context-create",
    ),
]
