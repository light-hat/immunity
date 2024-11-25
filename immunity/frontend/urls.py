from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("", login_required(views.DashBoardPageView.as_view())),
    path("agent/new/", login_required(views.DashBoardPageView.as_view())),
    path("app/", login_required(views.ApplicationPageView.as_view())),
    path("app/<slug:slug>/", login_required(views.ApplicationDetailPageView.as_view())),
    # path('change_pwd/', views.change_pwd, name='change_pwd'),
    # path('notes/', views.notes, name='notes'),
]
