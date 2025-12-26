from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path("register/",register_view,name='register'),
    path("login/",login_view,name='login'),
    path("logout/",logout_confirm, name='logout_confirm'),
    path("logout/confirm/",LogoutView.as_view(next_page='login'),name='logout'),
]