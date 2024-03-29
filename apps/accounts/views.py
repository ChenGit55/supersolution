from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm

def signup_view(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
        
    return render(request, 'accounts/signup.html', {'form' : form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password!'})
        
        login(request, user)

        return redirect('home')
    return render(request, 'accounts/login.html',{})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        redirect('login')
    return render(request, 'accounts/logout.html', {})

@login_required
def profile_view(request):
    user = request.user
    context = {
        'user' : user,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile_view(request):
    user = request.user

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)
        
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        initial_data = {'username': user.username}
        form = CustomUserChangeForm(initial=initial_data, instance=user)

    context = {
        'user' : user,
        'form' : form
    }
    return render(request, 'accounts/edit-profile.html', context)