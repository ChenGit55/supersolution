from django.shortcuts import render
from .models import Item, Stock

def inventory_view(request):
    all_items = Item.objects.all()
    stocks = Stock.objects.all()
    context = {
        'all_items' : all_items,
        'stocks' : stocks,
    }
    return render(request, 'inventory/inventory.html', context)
