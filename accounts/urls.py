from django.urls import path, include
from .views import *

urlpatterns = [
    path('', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
