from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Store
from .forms import StoreForm

@login_required
def store_view(request):
    store = Store.objects.all()
    context = {
        'store' : store
    }
    return render(request, 'stores/store.html', context)

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
