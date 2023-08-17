from django.shortcuts import render

def sales_view(request):
    return render(request, 'pos/sales.html', {})

def new_sale_view(request):    
    return render(request, 'pos/new-sale.html', {})