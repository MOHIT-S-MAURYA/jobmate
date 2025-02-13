#contractor/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='contractor-home'),
    path('profile/', views.profile_contractor, name='contractor-profile'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path('jobs/create/', views.create_job, name='create-job'),
    path('jobs/manage/', views.manage_jobs, name='manage-jobs'),
    path('jobs/delete/<int:job_id>/', views.delete_job, name='delete-job'),
    path('jobs/update-status/<int:job_id>/', views.update_job_status, name='update-job-status'),
    path('applications/', views.manage_applications, name='contractor-applications'),
    path('applications/<int:application_id>/update/', 
         views.update_application_status, 
         name='update-application'),
    path('work-history/', views.work_history, name='work-history'),
    path('find-workers/', views.find_workers, name='find-workers'),
]