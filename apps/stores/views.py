from django.shortcuts import render
from .models import Store
from .forms import StoreForm

def store_view(request):
    return render(request, 'stores/store.html', {})

def create_store_view(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = StoreForm()

    context = {
        'form' : form
    }
    return render(request, 'stores/store-creation.html', context)
