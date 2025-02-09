#worker/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'worker_home.html')

@login_required(login_url='/login/')
def profile_worker(request):
    return render(request, 'worker_profile.html')