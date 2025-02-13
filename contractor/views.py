#contractor/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import JobCreationForm
from .models import Contractor, Application

# Create your views here.

def home(request):
    return render(request, 'contractor_home.html')

@login_required(login_url='/login/')
def profile_contractor(request):
    return render(request, 'contractor_profile.html')

@login_required(login_url='/login/')
def create_job(request):
    if request.method == 'POST':
        form = JobCreationForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            # Get or create contractor profile for the user
            contractor, created = Contractor.objects.get_or_create(user=request.user)
            job.contractor = contractor
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('contractor-profile')
    else:
        form = JobCreationForm()
    return render(request, 'create_job.html', {'form': form})

@login_required(login_url='/login/')
def update_application_status(request, application_id):
    if request.method == 'POST':
        try:
            application = Application.objects.get(
                id=application_id,
                job__contractor__user=request.user
            )
            new_status = request.POST.get('status')
            if new_status in ['accepted', 'rejected']:
                application.status = new_status
                application.save()
                
                # Send notification to worker
                if new_status == 'accepted':
                    messages.success(request, 'Application accepted! The worker has been notified.')
                else:
                    messages.info(request, 'Application rejected. The worker has been notified.')
                    
                return redirect('contractor-applications')
                
        except Application.DoesNotExist:
            messages.error(request, 'Application not found or you do not have permission.')
    return redirect('contractor-applications')

@login_required(login_url='/login/')
def manage_applications(request):
    contractor = request.user.contractor
    job_filter = request.GET.get('job')
    status_filter = request.GET.get('status')
    
    # Get all applications for contractor's jobs
    applications_list = Application.objects.filter(
        job__contractor=contractor
    )
    
    # Apply filters if specified
    if job_filter:
        applications_list = applications_list.filter(job_id=job_filter)
    if status_filter:
        applications_list = applications_list.filter(status=status_filter)
    
    # Order by most recent first
    applications_list = applications_list.order_by('-applied_at')
    
    # Get all jobs for filter dropdown
    jobs = contractor.job_set.all()
    
    # Pagination
    paginator = Paginator(applications_list, 10)  # Show 10 applications per page
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
    
    # Get all jobs with their applications
    completed_jobs = Application.objects.filter(
        job__contractor=contractor,
        status='accepted'
    ).select_related('job', 'worker__user').order_by('-job__created_at')
    
    # Calculate statistics
    total_completed = completed_jobs.count()
    total_earnings = sum(job.job.wage for job in completed_jobs)
    
    # Pagination
    paginator = Paginator(completed_jobs, 10)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    
    return render(request, 'work_history.html', {
        'completed_jobs': jobs,
        'total_completed': total_completed,
        'total_earnings': total_earnings
    })