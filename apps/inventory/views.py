from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.stores.models import Store
from apps.accounts.models import CustomUser
from .models import Item
from .forms import ItemForm

@login_required
def inventory_view(request):
    items = Item.objects.all()
    stores = Store.objects.all()
    location_items = ""

    if request.method == 'POST':
        current_location = request.POST.get('location')

        if current_location== "":
            current_location= "Loja/Estoque, não definido"

        location_items = Item.objects.filter(location=current_location).all()
    else:
        current_location = ""

    context = {
        'items' : items,
        'stores' : stores,
        'current_location' : current_location,
        'location_items' : location_items,
    }
    return render(request, 'inventory/inventory.html', context)

@login_required
def add_product_view(request):
    form = ItemForm()
    items = Item.objects.all()
    stores = Store.objects.all()

    if request.method == 'POST':
        form = ItemForm(request.POST)

        if form.is_valid():
            product_id = request.POST.get('product')
            current_location= request.POST.get('location')

            if current_location== "" :
                current_location= "Loja/Estoque, não definido"

            quantity = int(request.POST['quantity'])
            existing_item = Item.objects.filter(product__id=product_id, location=current_location).first()

            if existing_item:
                existing_item.quantity += quantity
                existing_item.save()
            else:
                Item.objects.create(product_id=product_id, location=current_location, quantity=quantity)

        return redirect('add-product')

    context = {
        'form' : form,
        'items' : items,
        'stores' : stores,
    }
    return render(request, 'inventory/add-product.html', context)

def transfer_product_view(request):
    items = Item.objects.all()
    stores = Store.objects.all()
    location_items = ""
    
    if request.method == 'POST':
        current_location= request.POST.get('location')
        location_items = Item.objects.filter(location=current_location).all()

    context = {
        'items' : items,
        'stores' : stores,
        'location_items' : location_items,
    }
    return render(request, 'inventory/transfer-product.html', context)