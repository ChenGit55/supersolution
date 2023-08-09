from django.shortcuts import render
from .forms import AddProductForm

def product_list_view(request):
    return render(request,'products/all-products.html',{})

def new_product_view(request):
    if request.method == "POST":
        form = AddProductForm(request.POST)
    else:
        form = AddProductForm()

    context = {
        'form' : form
    }
    return render(request, 'products/new-product.html', context)