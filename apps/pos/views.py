from django.shortcuts import render

def sales_view (request):    
    return render (request, 'pos/sale.html', {})

