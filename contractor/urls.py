#contractor/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='contractor-home'),
    path('profile/', views.profile_contractor, name='contractor-profile'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path('jobs/create/', views.create_job, name='create-job'),
    path('jobs/edit/<int:job_id>/', views.edit_job, name='edit-job'),
    path('jobs/delete/<int:job_id>/', views.delete_job, name='delete-job'),
    path('jobs/update-status/<int:job_id>/', views.update_job_status, name='update-job-status'),
    path('applications/', views.manage_applications, name='manage-applications'),
    path('applications/<int:application_id>/update/', views.update_application_status, name='update-application-status'),
    path('find-workers/', views.find_workers, name='find-workers'),
    path('work-history/', views.work_history, name='work-history'),
    path('jobs/manage/', views.manage_jobs, name='manage-jobs'),  # Add this line
]