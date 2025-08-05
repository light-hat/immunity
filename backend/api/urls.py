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
    path(
        "users/export-preferences/", views.export_preferences, name="export_preferences"
    ),
    path(
        "users/import-preferences/", views.import_preferences, name="import_preferences"
    ),
    path("users/stats/", views.user_stats, name="user_stats"),
    # Legacy endpoints for compatibility
    path("users/get-preferences/", views.user_preferences, name="get_preferences"),
    path("users/save-preferences/", views.user_preferences, name="save_preferences"),
]
