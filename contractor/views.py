#contractor/views.py

from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'contractor_home.html')