from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.stores.models import Store
from .models import Item, Stock
from .forms import ItemForm

@login_required
def inventory_view(request):
    items = Item.objects.all()
    context = {
        'items' : items,
    }
    return render(request, 'inventory/inventory.html', context)

@login_required
def add_product_view(request):
    form = ItemForm()
    items = Item.objects.all()
    stores = Store.objects.all()
    stocks = Stock.objects.all()

    if request.method == 'POST':
        form = ItemForm(request.POST)

        if form.is_valid():
            product_id = request.POST.get('product')
            location = request.POST.get('location')
            if location == "" :
                location = "Loja/Estoque, não definido"
            quantity = int(request.POST['quantity'])
            existing_item = Item.objects.filter(product__id=product_id, location=location).first()

            if existing_item:
                existing_item.quantity += quantity
                existing_item.save()
            else:
                Item.objects.create(product_id=product_id, location=location, quantity=quantity)

        return redirect('add-product')


    context = {
        'form' : form,
        'items' : items,
        'stores' : stores,
        'stocks' : stocks,
    }
    return render(request, 'inventory/add-product.html', context)

def transfer_product_view(request):
    items = Item.objects.all()
    stores = Store.objects.all()
    stocks = Stock.objects.all()
    if request.method == 'POST':
        location = request.POST.get('location')
        location_items = Item.objects.filter(location=location).all()
        print(location_items)
    context = {
        'items' : items,
        'stores' : stores,
        'stocks' : stocks,
    }
    return render(request, 'inventory/transfer-product.html', context)