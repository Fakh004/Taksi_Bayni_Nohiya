from django.urls import path
from .views import register_view, login_view, logout_confirm_view, logout_view


urlpatterns = [
    path("register/", register_view, name='register'),
    path("login/", login_view, name='login'),
    path("logout/", logout_confirm_view, name='logout_confirm'),
    path("logout/confirm/", logout_view, name='logout'),
]
