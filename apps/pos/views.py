from django.shortcuts import render
from .models import Sale, SaleItem
from .forms import SaleItemForm, DateForm
from apps.products.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .serializers import SaleSerializer, SaleItemSerializer
from rest_framework import generics, viewsets
from django.utils import timezone
from datetime import datetime

now = timezone.now()
today = now.strftime("%d/%m/%Y")

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
    form = DateForm()
    selected_date = today
    print(today, timezone.now())
    selected_date_sales = Sale.objects.filter(date__date=now)
    if request.method == 'POST':
        selected_date = request.POST.get('date')
        f_date = datetime.strptime(selected_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        selected_date_sales = Sale.objects.filter(date__date=f_date)


    context = {
        'sales' : sales,
        'form' : form,
        'selected_date' : selected_date,
        'selected_date_sales' : selected_date_sales,
    }
    return render(request, 'pos/sales.html', context)

@login_required
def new_sale_view(request):
    form = SaleItemForm()
    user = request.user
    store = request.user.store

    if request.method == 'POST':
        sale = Sale.objects.create(user=user, store=store)
        form = SaleItemForm(request.POST)

        product_ids = request.POST.get('product_ids')
        product_prices = request.POST.get('product_prices')
        quantities = request.POST.get('quantities')

        product_ids = product_ids.split(',')
        product_prices = product_prices.split(',')
        quantities = quantities.split(',')

        for index in range(len(product_ids)):
            id = Product.objects.get(pk=product_ids[index])
            SaleItem.objects.create(
                sale = sale,
                product = id,
                price = float(product_prices[index]),
                quantity = int(quantities[index]),
            )

    context = {
        'form' : form,
    }
    return render(request, 'pos/new-sale.html', context)