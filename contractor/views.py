#contractor/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import JobCreationForm, WorkRequestForm
from dailywage_website.forms import CustomUserUpdateForm, ContractorProfileForm  # Correct import
from .models import Contractor, Application, Job, WorkRequest
from worker.models import Skill, Worker
from django.db.models import Q

# Create your views here.

def home(request):
    return render(request, 'contractor_home.html')

@login_required(login_url='/login/')
def profile_contractor(request):
    contractor = request.user.contractor
    
    # Get counts of active jobs and completed projects
    active_jobs_count = Job.objects.filter(contractor=contractor, status='open').count()
    completed_projects_count = Job.objects.filter(contractor=contractor, status='closed').count()
    
    # Get recent applications for the contractor's jobs
    recent_applications = Application.objects.filter(
        job__contractor=contractor
    ).order_by('-applied_at')[:3]
    
    # Get all jobs posted by the contractor
    jobs = Job.objects.filter(contractor=contractor).order_by('-created_at')
    
    return render(request, 'contractor_profile.html', {
        'active_jobs_count': active_jobs_count,
        'completed_projects_count': completed_projects_count,
        'recent_applications': recent_applications,
        'jobs': jobs
    })

@login_required(login_url='/login/')
def create_job(request):
    if request.method == 'POST':
        form = JobCreationForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.contractor = request.user.contractor
            job.save()
            messages.success(request, 'Job created successfully!')
            return redirect('manage-jobs')
    else:
        form = JobCreationForm()
    return render(request, 'create_job.html', {'form': form})

@login_required(login_url='/login/')
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, contractor=request.user.contractor)
    if request.method == 'POST':
        form = JobCreationForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('manage-jobs')
    else:
        form = JobCreationForm(instance=job)
    return render(request, 'edit_job.html', {'form': form, 'job': job})

@login_required(login_url='/login/')
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, contractor=request.user.contractor)
    job.delete()
    messages.success(request, 'Job deleted successfully!')
    return redirect('manage-jobs')

@login_required(login_url='/login/')
def update_job_status(request, job_id):
    job = get_object_or_404(Job, id=job_id, contractor=request.user.contractor)
    job.status = 'closed'
    job.save()
    messages.success(request, 'Job status updated to complete!')
    return redirect('manage-jobs')

@login_required(login_url='/login/')
def update_application_status(request, application_id):
    application = get_object_or_404(Application, id=application_id, job__contractor=request.user.contractor)
    new_status = request.POST.get('status')
    if new_status in ['accepted', 'rejected']:
        application.status = new_status
        application.save()
        messages.success(request, f'Application {new_status} successfully!')
    else:
        messages.error(request, 'Invalid status update.')
    return redirect('manage-applications')

@login_required(login_url='/login/')
def manage_applications(request):
    contractor = request.user.contractor
    job_filter = request.GET.get('job')
    status_filter = request.GET.get('status')
    
    applications_list = Application.objects.filter(job__contractor=contractor)
    
    if job_filter:
        applications_list = applications_list.filter(job_id=job_filter)
    if status_filter:
        applications_list = applications_list.filter(status=status_filter)
    
    applications_list = applications_list.order_by('-applied_at')
    
    jobs = contractor.job_set.all()
    
    paginator = Paginator(applications_list, 10)
    page = request.GET.get('page')
    applications = paginator.get_page(page)
    
    return render(request, 'manage_applications.html', {
        'applications': applications,
        'jobs': jobs,
        'current_job': job_filter,
        'current_status': status_filter
    })

@login_required(login_url='/login/')
def work_history(request):
    contractor = request.user.contractor
    
    # Get all jobs posted by the contractor
    jobs = Job.objects.filter(contractor=contractor).order_by('-created_at')
    
    # Separate active jobs and completed projects
    active_jobs = jobs.filter(status='open')
    completed_projects = jobs.filter(status='closed')
    
    # Pagination for active jobs
    paginator_active = Paginator(active_jobs, 5)  # Show 5 active jobs per page
    page_active = request.GET.get('page_active')
    active_jobs = paginator_active.get_page(page_active)
    
    # Pagination for completed projects
    paginator_completed = Paginator(completed_projects, 5)  # Show 5 completed projects per page
    page_completed = request.GET.get('page_completed')
    completed_projects = paginator_completed.get_page(page_completed)
    
    return render(request, 'work_history.html', {
        'active_jobs': active_jobs,
        'completed_projects': completed_projects,
    })

@login_required(login_url='/login/')
def edit_profile(request):
    contractor = request.user.contractor
    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, instance=request.user)
        contractor_form = ContractorProfileForm(request.POST, instance=contractor)
        if user_form.is_valid() and contractor_form.is_valid():
            user_form.save()
            contractor_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('contractor-profile')
    else:
        user_form = CustomUserUpdateForm(instance=request.user)
        contractor_form = ContractorProfileForm(instance=contractor)
    
    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'contractor_form': contractor_form
    })

@login_required(login_url='/login/')
def find_workers(request):
    query = Q()
    
    # Search filters
    search = request.GET.get('search')
    location = request.GET.get('location')
    min_experience = request.GET.get('min_experience')
    skill_filter = request.GET.get('skill')
    
    if search:
        query &= Q(user__first_name__icontains=search) | Q(user__last_name__icontains=search) | Q(user__email__icontains=search)
    if location:
        query &= Q(location__icontains=location)
    if min_experience:
        query &= Q(experience__gte=min_experience)
    if skill_filter:
        query &= Q(skills__name__icontains=skill_filter)
    
    workers = Worker.objects.filter(query).distinct().order_by('-experience')
    paginator = Paginator(workers, 10)
    page = request.GET.get('page')
    workers = paginator.get_page(page)
    
    # Get all unique skills for filter dropdown
    all_skills = Skill.objects.all()
    
    # Get jobs that are not taken
    available_jobs = Job.objects.filter(contractor=request.user.contractor, status='open').exclude(
        id__in=Application.objects.filter(status='accepted').values_list('job_id', flat=True)
    )
    
    if request.method == 'POST':
        work_request_form = WorkRequestForm(request.POST, contractor=request.user.contractor)
        if work_request_form.is_valid():
            work_request = work_request_form.save(commit=False)
            work_request.contractor = request.user.contractor
            work_request.worker = Worker.objects.get(user_id=request.POST.get('worker_id'))
            work_request.save()
            messages.success(request, 'Work request sent successfully!')
            return redirect('find-workers')
    else:
        work_request_form = WorkRequestForm(contractor=request.user.contractor)
    
    return render(request, 'find_workers.html', {
        'workers': workers,
        'all_skills': all_skills,
        'current_filters': request.GET,
        'work_request_form': work_request_form,
        'available_jobs': available_jobs
    })

@login_required(login_url='/login/')
def manage_jobs(request):
    contractor = request.user.contractor
    
    # Get all jobs posted by the contractor
    jobs = Job.objects.filter(contractor=contractor).order_by('-created_at')
    
    return render(request, 'manage_jobs.html', {
        'jobs': jobs
    })

@login_required(login_url='/login/')
def delete_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id, contractor=request.user.contractor)
        job.delete()
        messages.success(request, 'Job deleted successfully!')
    except Job.DoesNotExist:
        messages.error(request, 'Job not found or you do not have permission.')
    return redirect('manage-jobs')

@login_required(login_url='/login/')
def update_job_status(request, job_id):
    try:
        job = Job.objects.get(id=job_id, contractor=request.user.contractor)
        job.status = 'closed'
        job.save()
        
        # Update the status of related applications
        Application.objects.filter(job=job, status='pending').update(status='rejected')
        
        messages.success(request, 'Job status updated to complete and related applications updated!')
    except Job.DoesNotExist:
        messages.error(request, 'Job not found or you do not have permission.')
    return redirect('manage-jobs')