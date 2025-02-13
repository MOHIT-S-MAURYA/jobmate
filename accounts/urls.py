from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile_redirect/', views.profile_redirect, name='profile_redirect'),
    path('profile/setup/', views.profile_setup, name='profile-setup'),
]