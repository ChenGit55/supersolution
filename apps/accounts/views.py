from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout
from .forms import CustomUserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    context = { 'form' : form }
    return render(request, 'accounts/signup.html', context)

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is None:
            context = {'error': 'Invalid username or password!'}
            return render(request, 'accounts/login.html', context)
        login(request, user)
        return redirect('/admin/') 
    return render(request, 'accounts/login.html',{})