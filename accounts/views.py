from django.shortcuts import render

# Create your views here.
def signup(request):
    return render(request, 'signup.html')

def login_view(request):
    return render(request, 'login.html')