from django.urls import path
from .views import login_view, signup_view, logout_view, profile_view, edit_profile_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('edit/', edit_profile_view, name='edit-profile'),
]