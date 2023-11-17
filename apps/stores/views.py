from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Store
from .forms import StoreForm

@login_required
def store_view(request):
    stores = Store.objects.all().order_by('name')
    context = {
        'stores' : stores
    }
    return render(request, 'stores/stores.html', context)

@login_required
def create_store_view(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save()
    else:
        form = StoreForm()

    context = {
        'form' : form
    }
    return render(request, 'stores/store-creation.html', context)
