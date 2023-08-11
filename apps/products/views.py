from django.shortcuts import render, redirect
from .forms import AddProductForm
from .models import Product

def product_list_view(request):
    products = Product.objects.all()
    print(products)
    context = {'products' : products}
    return render(request,'products/products.html', context)

def new_product_view(request):
    if request.method == "POST":
        form = AddProductForm(request.POST)
        if form.is_valid:            
            form.save()
            return redirect ('products')
    else:
        form = AddProductForm()

    context = {
        'form' : form
    }
    return render(request, 'products/new-product.html', context)