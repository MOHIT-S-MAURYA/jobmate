#worker/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from contractor.models import Job, Application
from .models import Worker, Skill, WorkerSkill
from .forms import WorkerSkillForm

# Create your views here.
def home(request):
    return render(request, 'worker_home.html')

@login_required(login_url='/login/')
def profile_worker(request):
    return render(request, 'worker_profile.html')

@login_required(login_url='/login/')
def find_jobs(request):
    query = Q(status='open')
    
    # Search filters
    search = request.GET.get('search')
    location = request.GET.get('location')
    min_wage = request.GET.get('min_wage')
    
    if search:
        query &= Q(title__icontains=search) | Q(required_skills__icontains=search)
    if location:
        query &= Q(location__icontains=location)
    if min_wage:
        query &= Q(wage__gte=min_wage)
    
    jobs = Job.objects.filter(query).order_by('-created_at')
    return render(request, 'find_jobs.html', {'jobs': jobs})

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