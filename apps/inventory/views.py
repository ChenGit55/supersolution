from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.stores.models import Store
from .models import Item, Stock
from .forms import ItemForm

@login_required
def inventory_view(request):
    all_items = Item.objects.all()
    stores = Store.objects.all()
    stocks = Stock.objects.all()
    form = ItemForm(request.POST)

    items_by_store = {}

    for store in stores:
        items = Item.objects.filter(store=store)
        items_by_store[store] = items

    if request.method == 'POST':
        form.save()
    context = {
        'all_items' : all_items,
        'stores' : stores,
        'items_by_store' : items_by_store,
        'stocks' : stocks,
        'form' : form,
    }
    return render(request, 'inventory/inventory.html', context)
