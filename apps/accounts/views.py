from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from apps.stores.models import Store

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        stores = Store.objects.all()
        if stores.exists() and form.is_valid():
            msg = ''
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            return redirect('login')
        else:
            msg = "Precisa cadastrar uma loja primeiro!"
    else:
        msg = '' 
        form = CustomUserCreationForm()
    context = {
         'form' : form,
         'msg' : msg,
         'stores' : stores,
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