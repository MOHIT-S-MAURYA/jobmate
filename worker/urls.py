#worker/views.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='worker-home'),
    path('profile/', views.profile_worker, name='worker-profile'),
]