from django.shortcuts import render
from .models import Item 

def inventory_view(request):
    all_items = Item.objects.all()

    context = {
        "all_items" : all_items,
    }
    return render(request, 'inventory/inventory.html', context)
