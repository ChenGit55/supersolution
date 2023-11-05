from django.shortcuts import render
from .models import Sale, SaleItem, PaymentMethod
from .forms import SaleItemForm, DateForm
from apps.products.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .serializers import SaleSerializer, SaleItemSerializer
from rest_framework import generics, viewsets
from django.utils import timezone
from datetime import datetime
from django.db.models import Sum

now = timezone.now().astimezone(timezone.get_current_timezone())
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
    print(now)
    if request.user.is_superuser:
        selected_date_sales = Sale.objects.filter(date__date=now)
    else:
        selected_date_sales = Sale.objects.filter(date__date=now, user=request.user)
    total_daily_sales = selected_date_sales.aggregate(total=Sum('total'))['total']
    if request.method == 'POST':
        selected_date = request.POST.get('date')
        f_date = datetime.strptime(selected_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        if request.user.is_superuser:
            selected_date_sales = Sale.objects.filter(date__date=f_date)
        else:
            selected_date_sales = Sale.objects.filter(date__date=f_date, user=request.user)
        total_daily_sales = selected_date_sales.aggregate(total=Sum('total'))['total']


    context = {
        'sales' : sales,
        'form' : form,
        'selected_date' : selected_date,
        'selected_date_sales' : selected_date_sales,
        'total_daily_sales' : total_daily_sales,
    }
    return render(request, 'pos/sales.html', context)

@login_required
def new_sale_view(request):
    form = SaleItemForm()
    user = request.user
    store = request.user.store
    payment_methods = PaymentMethod.objects.all()

    if request.method == 'POST':
        payment_method_id = request.POST.get('payment-method')
        payment_method = PaymentMethod.objects.get(id=payment_method_id)

        sale = Sale.objects.create(user=user, store=store, payment_method=payment_method)
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
        sale.save()

    context = {
        'form' : form,
        'payment_methods' : payment_methods
    }
    return render(request, 'pos/new-sale.html', context)