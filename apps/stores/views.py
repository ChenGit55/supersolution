from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Store
from .forms import StoreForm
from apps.products.models import Product
from apps.inventory.models import Item

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
            products = Product.objects.all()
            store = form.save()
            for product in products:
                Item.objects.create(
                    product = product,
                    store = store,
                    quantity=0,
                )
            return redirect('stores')
    else:
        form = StoreForm()

    context = {
        'form' : form
    }
    return render(request, 'stores/store-creation.html', context)
