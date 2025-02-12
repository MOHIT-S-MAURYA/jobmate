#contractor/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='contractor-home'),
    path('profile/', views.profile_contractor, name='contractor-profile'),
    path('jobs/create/', views.create_job, name='create-job'),
]