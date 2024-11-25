from agent_api import views
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("upload", csrf_exempt(views.BaseApiView.as_view({"post": "upload"}))),
]
