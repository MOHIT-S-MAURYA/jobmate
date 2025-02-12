#contractor/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import JobCreationForm
from .models import Contractor

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