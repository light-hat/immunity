"""
Определение доступных url-адресов REST API.
"""

from api.v1.viewsets import (FolderViewSet, FileViewSet)
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'user', UserViewSet, basename='user')
router.register(r'folder', FolderViewSet, basename='folder')
router.register(r'file', FileViewSet, basename='file')

urlpatterns = [
    path('', include(router.urls)),
]
