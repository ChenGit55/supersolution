from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm

def signup_view(request):
    form = CustomUserCreationForm()    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            return redirect('login')

    context = {
         'form' : form,
    }
    return render(request, 'accounts/signup.html', context)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            context = {'error': 'Invalid username or password!'}
            return render(request, 'accounts/login.html', context)
        login(request, user)
        return redirect('home') 
    return render(request, 'accounts/login.html',{})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        redirect('login')
    return render(request, 'accounts/logout.html', {})

def profile_view(request):
    user = request.user
    context = {
        'user' : user
    }
    return render(request, 'accounts/profile.html', context)