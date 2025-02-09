#contractor/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'contractor_home.html')

@login_required(login_url='/login/')
def profile_contractor(request):
    return render(request, 'contractor_profile.html')