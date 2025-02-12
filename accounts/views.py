from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from dailywage_website.forms import CustomUserUpdateForm, WorkerProfileForm, ContractorProfileForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from worker.models import Worker
from contractor.models import Contractor

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Signup successful! Welcome to JobMate.')
            return redirect('profile-setup')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful! Welcome back.')
            return redirect('profile_redirect')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful! See you again.')
    return redirect('home')

@login_required(login_url='/login/')
def profile_redirect(request):
    if request.user.role == 'worker':
        return redirect('worker-profile')
    elif request.user.role == 'contractor':
        return redirect('contractor-profile')
    else:
        messages.error(request, 'Invalid role.')
        return redirect('home')

@login_required
def profile_setup(request):
    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, instance=request.user)
        
        if request.user.role == 'worker':
            profile_form = WorkerProfileForm(request.POST)
        else:
            profile_form = ContractorProfileForm(request.POST)
            
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            
            messages.success(request, 'Profile completed successfully!')
            return redirect('profile_redirect')
    else:
        user_form = CustomUserUpdateForm(instance=request.user)
        if request.user.role == 'worker':
            profile_form = WorkerProfileForm()
        else:
            profile_form = ContractorProfileForm()
    
    return render(request, 'profile_setup.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

