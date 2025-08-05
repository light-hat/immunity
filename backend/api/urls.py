from django.urls import include, path
from . import views

urlpatterns = [
    path("auth/", include("djoser.urls")),
    # path("auth/", include("djoser.urls.jwt")),  # Commented out to use custom JWT endpoints
    
    # Custom JWT endpoints with HttpOnly cookies
    path("auth/jwt/create/", views.jwt_create, name="jwt-create"),
    path("auth/jwt/refresh/", views.jwt_refresh, name="jwt-refresh"),
    path("auth/jwt/logout/", views.jwt_logout, name="jwt-logout"),
    
    # User preferences and account management
    path("users/preferences/", views.user_preferences, name="user_preferences"),
    path("users/change-email/", views.change_email, name="change_email"),
    path("users/reset-preferences/", views.reset_preferences, name="reset_preferences"),
    path("users/export-preferences/", views.export_preferences, name="export_preferences"),
    path("users/import-preferences/", views.import_preferences, name="import_preferences"),
    path("users/stats/", views.user_stats, name="user_stats"),
    
    # Legacy endpoints for compatibility
    path("users/get-preferences/", views.user_preferences, name="get_preferences"),
    path("users/save-preferences/", views.user_preferences, name="save_preferences"),
    
    # path(
    #     "project/", csrf_exempt(ProjectAPIView.as_view({"get": "get", "post": "post"}))
    # ),
    # path(
    #     "project/<int:pk>/",
    #     csrf_exempt(
    #             ProjectAPIView.as_view(
    #                 {"get": "retrieve", "put": "put", "delete": "delete"}
    #             )
    #         )
    #     ),
    # ),
    # path("project/filter/", csrf_exempt(ProjectAPIView.as_view({"get": "filter"}))),
    # path("project/<int:pk>/config/", csrf_exempt(ProjectAPIView.as_view({"get": "retrieve_config"}))),
    # path("project/<int:pk>/libs/", csrf_exempt(ProjectAPIView.as_view({"get": "retrieve_libs"}))),
    # path(
    #     "vulnerability/", csrf_exempt(VulnerabilityAPIView.as_view({"get": "filter"}))
    # ),
    # path("dataset/", csrf_exempt(DatasetAPIView.as_view({"get": "filter"}))),
    # path("dataset/counters/", csrf_exempt(DatasetAPIView.as_view({"get": "retrieve_counters"}))),
    # path("dataset/markup/", csrf_exempt(DatasetAPIView.as_view({"post": "post"}))),
    # path("context/", csrf_exempt(ContextAPIView.as_view({"get": "filter"}))),
    # path("context/<int:pk>/", csrf_exempt(ContextDetailAPIView.as_view({"get": "retrieve"}))),
]
