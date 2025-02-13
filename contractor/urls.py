#contractor/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='contractor-home'),
    path('profile/', views.profile_contractor, name='contractor-profile'),
    path('jobs/create/', views.create_job, name='create-job'),
    path('applications/', views.manage_applications, name='contractor-applications'),
    path('applications/<int:application_id>/update/', 
         views.update_application_status, 
         name='update-application'),
    path('work-history/', views.work_history, name='work-history'),
]