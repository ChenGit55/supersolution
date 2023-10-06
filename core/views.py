from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_view (request):
    return render(request, 'core/home.html',{})

def start_view(request):
    context = {}
    return render(request, 'start-page.html', context)