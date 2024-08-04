"""
Конфигурация URL-адреса для основного проекта.
"""

from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from os import environ
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

api_url = environ.get('API_URL')
api_port = environ.get('API_PORT')

schema_view = get_schema_view(
    openapi.Info(
        title="OpenDisk API",
        default_version='v1',
        description="REST API.",
    ),
    url=f"http://{api_url}:{api_port}",
    public=True,  # False
    permission_classes=(permissions.AllowAny,),
    # permission_classes=(permissions.IsAdminUser,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.v1.urls')),
    path('swagger/<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view().with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view().with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
