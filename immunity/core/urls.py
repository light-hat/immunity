"""
Конфигурация URL-адреса для основного проекта.
"""

from os import environ
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

api_url = environ.get('API_URL')
api_port = environ.get('API_PORT')

'''schema_view = get_schema_view(
    openapi.Info(
        title="OpenDisk API",
        default_version='v1',
        description="REST API.",
    ),
    url=f"http://{api_url}:{api_port}",
    public=True,  # False
    permission_classes=(permissions.AllowAny,),
    # permission_classes=(permissions.IsAdminUser,),
)'''

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('frontend.urls')),
]
