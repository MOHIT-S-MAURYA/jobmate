#worker/views.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='worker-home'),
    path('profile/', views.profile_worker, name='worker-profile'),
    path('jobs/', views.find_jobs, name='find-jobs'),
    path('jobs/apply/<int:job_id>/', views.apply_job, name='apply-job'),
    path('skills/manage/', views.manage_skills, name='manage-skills'),
]