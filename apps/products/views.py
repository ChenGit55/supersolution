from django.shortcuts import render, redirect
from .forms import AddProductForm
from .models import Product
from django.contrib.auth.decorators import login_required

@login_required
def product_list_view(request):
    products = Product.objects.all()
    
    return render(request,'products/products.html', {'products' : products})

@login_required
def new_product_view(request):

    if request.method == "POST":
        form = AddProductForm(request.POST)

        if form.is_valid:
            form.save()
            return redirect ('products')
    else:
        form = AddProductForm()

    return render(request, 'products/new-product.html', {'form' : form})

@login_required
def product_detail_view(request, code):
    details = Product.objects.get(code=code)
    context = {'details' : details }  

    return render(request, 'products/product-detail.html', context)