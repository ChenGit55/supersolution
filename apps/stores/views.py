from django.shortcuts import render
from .models import Store

def store_view(request):
    return render(request, 'stores/store.html', {})
