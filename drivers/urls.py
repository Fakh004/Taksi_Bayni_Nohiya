from django.urls import path
from .views import *


urlpatterns = [
    path('', driver_list, name='home'),
    path('driver_list/', driver_list, name='driver_list'),
    path('create/', driver_create, name='driver_create'),
    path('<int:driver_id>/', driver_detail, name='driver_detail'),
    path('<int:driver_id>/update/', driver_update, name='driver_update'),
    path('<int:driver_id>/delete/', driver_delete_view, name='driver_delete'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', profile_update, name='profile_update'),
]