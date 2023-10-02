from django.shortcuts import render
from .models import Sale, SaleItem
from apps.products.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .serializers import SaleSerializer, SaleItemSerializer
from rest_framework import generics, viewsets


class SaleList(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class SaleViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class SaleItemList(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer

class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer

@login_required
def sales_view(request):
    sales = Sale.objects.all().order_by('-id')
    context = {
        'sales' : sales,
    }
    return render(request, 'pos/sales.html', context)

@login_required
def new_sale_view(request):
    
    if request.method == 'POST':
        user = request.user
        store = request.user.store
        sale = Sale.objects.create(user=user)
        
        product_fields = [key for key in request.POST if key.startswith('product-')]
        print(product_fields)
        
        products_list = []
        
        current_index = None
        
        for field_name in product_fields:
            parts = field_name.split('-')
            if len(parts) == 3 and parts[1].isdigit():
                index = int(parts[1]) - 1
                product_id = request.POST.get(f'product-{index+1}-id')
                title = request.POST.get(f'product-{index+1}-title')
                price = request.POST.get(f'product-{index + 1}-price')
                quantity = request.POST.get(f'product-{index + 1}-quantity')
                title = title or None
                if index != current_index:              
                    products_list.append((sale, product_id, title, price, quantity))
                    current_index = index

        current_index = None
               
        
        for sale, product_id, title, price, quantity in products_list:
            id = Product.objects.get(pk=product_id)
            
            SaleItem.objects.create(
                sale = sale,
                product = id,
                quantity = int(quantity),
                price = float(price),
            )

        context = {
            'user': user,
            'products': Product.objects.all(),
            'store': store,
        }

        return render(request, 'pos/new-sale.html', context)
    
    return render(request, 'pos/new-sale.html',{})
