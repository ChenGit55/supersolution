from django.shortcuts import render, redirect
from .forms import AddProductForm
from .models import Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .serializers import ProductSerializer
from rest_framework import generics

class ProductList(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@login_required
def product_list_view(request, code=None):
    products = Product.objects.all()
    context = {
        'products' : products,
        }
    return render(request,'products/products.html', context)

@login_required
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

@login_required
def product_detail_view(request, code):
    details = Product.objects.get(code=code)
    context = {'details' : details }
    return render(request, 'products/product-detail.html', context)