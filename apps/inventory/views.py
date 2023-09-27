from django.shortcuts import render

def inventory_view(request):
    return render(request, 'inventory/inventory.html',{})
