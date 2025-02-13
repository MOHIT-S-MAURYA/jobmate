#worker/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from contractor.models import Job, Application, WorkRequest
from .models import Worker, Skill, WorkerSkill
from .forms import WorkerSkillForm
from datetime import datetime, timedelta

# Create your views here.
def home(request):
    return render(request, 'worker_home.html')

@login_required(login_url='/login/')
def profile_worker(request):
    worker = request.user.worker
    
    recent_applications = Application.objects.filter(worker=worker).order_by('-applied_at')[:3]
    
    return render(request, 'worker_profile.html', {
        'recent_applications': recent_applications,
    })

@login_required(login_url='/login/')
def find_jobs(request):
    query = Q(status='open')
    
    # Enhanced search filters
    search = request.GET.get('search')
    location = request.GET.get('location')
    min_wage = request.GET.get('min_wage')
    skill_filter = request.GET.get('skill')
    date_posted = request.GET.get('date_posted')
    
    if search:
        query &= Q(title__icontains=search) | Q(description__icontains=search) | Q(required_skills__icontains=search)
    if location:
        query &= Q(location__icontains=location)
    if min_wage:
        query &= Q(wage__gte=min_wage)
    if skill_filter:
        query &= Q(required_skills__icontains=skill_filter)
    if date_posted:
        if date_posted == 'today':
            query &= Q(created_at__date=datetime.now().date())
        elif date_posted == 'week':
            query &= Q(created_at__gte=datetime.now() - timedelta(days=7))
        elif date_posted == 'month':
            query &= Q(created_at__gte=datetime.now() - timedelta(days=30))
    
    # Exclude jobs that have been accepted by a worker
    accepted_jobs = Application.objects.filter(status='accepted').values_list('job_id', flat=True)
    query &= ~Q(id__in=accepted_jobs)
    
    jobs = Job.objects.filter(query).order_by('-created_at')
    paginator = Paginator(jobs, 10)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    
    # Get all unique skills for filter dropdown
    all_skills = Skill.objects.all()
    
    return render(request, 'find_jobs.html', {
        'jobs': jobs,
        'all_skills': all_skills,
        'current_filters': request.GET
    })

@login_required(login_url='/login/')
def apply_job(request, job_id):
    if request.method == 'POST':
        try:
            job = Job.objects.get(id=job_id, status='open')
            # Check if already applied
            if not Application.objects.filter(worker=request.user.worker, job=job).exists():
                Application.objects.create(
                    worker=request.user.worker,
                    job=job,
                    status='pending'
                )
                messages.success(request, 'Application submitted successfully!')
            else:
                messages.warning(request, 'You have already applied for this job.')
        except Job.DoesNotExist:
            messages.error(request, 'Job not found or no longer available.')
    return redirect('find-jobs')

@login_required(login_url='/login/')
def manage_skills(request):
    worker, created = Worker.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = WorkerSkillForm(request.POST, worker=worker)
        if form.is_valid():
            selected_skills = form.cleaned_data['skills']
            
            # Remove existing skills
            WorkerSkill.objects.filter(worker=worker).delete()
            
            # Add new skills
            for skill in selected_skills:
                WorkerSkill.objects.create(worker=worker, skill=skill)
            
            messages.success(request, 'Skills updated successfully!')
            return redirect('worker-profile')
    else:
        form = WorkerSkillForm(worker=worker)
    
    return render(request, 'manage_skills.html', {
        'form': form,
        'all_skills': Skill.objects.all().order_by('category', 'name')
    })

@login_required(login_url='/login/')
def applications(request):
    status_filter = request.GET.get('status', '')
    
    # Get all applications for the worker
    applications_list = Application.objects.filter(worker=request.user.worker)
    
    # Apply status filter if specified
    if status_filter:
        applications_list = applications_list.filter(status=status_filter)
    
    # Order by most recent first
    applications_list = applications_list.order_by('-applied_at')
    
    # Pagination
    paginator = Paginator(applications_list, 10)  # Show 10 applications per page
    page = request.GET.get('page')
    applications = paginator.get_page(page)
    
    return render(request, 'worker_applications.html', {
        'applications': applications,
        'status': status_filter
    })

@login_required(login_url='/login/')
def manage_work_requests(request):
    worker = request.user.worker
    
    # Get all work requests for the worker
    work_requests = WorkRequest.objects.filter(worker=worker, status='pending').order_by('-created_at')
    
    if request.method == 'POST':
        work_request_id = request.POST.get('work_request_id')
        action = request.POST.get('action')
        
        try:
            work_request = WorkRequest.objects.get(id=work_request_id, worker=worker)
            if action == 'accept':
                work_request.status = 'accepted'
                # Create an application for the accepted work request
                Application.objects.create(
                    worker=worker,
                    job=work_request.job,
                    status='accepted'
                )
                messages.success(request, 'Work request accepted successfully!')
            elif action == 'reject':
                work_request.status = 'rejected'
                messages.success(request, 'Work request rejected successfully!')
            work_request.save()
        except WorkRequest.DoesNotExist:
            messages.error(request, 'Work request not found or you do not have permission.')
    
    return render(request, 'manage_work_requests.html', {
        'work_requests': work_requests
    })