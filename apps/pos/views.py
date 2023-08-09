from django.shortcuts import render

def sale_view (request):    
    return render (request, 'pos/sale.html', {})

