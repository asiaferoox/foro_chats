# users/urls.py

from django.urls import path
from .views      import signup_view, profile_view, profile_update_view

app_name = 'users'

urlpatterns = [
    path('signup/',       signup_view,          name='signup'),
    path('profile/',      profile_view,         name='profile'),
    path('profile/edit/', profile_update_view,  name='profile_edit'),
]
