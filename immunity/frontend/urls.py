from . import views
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    #path('', views.index, name='index'),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    #path('change_pwd/', views.change_pwd, name='change_pwd'),
    #path('notes/', views.notes, name='notes'),
]
