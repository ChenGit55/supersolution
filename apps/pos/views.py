from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Sale, SaleItem, PaymentMethod, Payment
from .forms import SaleItemForm, DateForm
from apps.products.models import Product
from apps.inventory.models import Item
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from django.db.models import Sum
import json

now = timezone.now().astimezone(timezone.get_current_timezone())
today = now.strftime("%d/%m/%Y")


@login_required
def sales_view(request):
    sales = Sale.objects.all().order_by('-id')
    payments = Payment.objects.all()
    form = DateForm()
    selected_date = today

    if request.user.is_superuser:
        selected_date_sales = Sale.objects.filter(date__date=now)
    else:
        selected_date_sales = Sale.objects.filter(date__date=now, user=request.user, store=request.user.store)
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
        'payments' : payments,
        'form' : form,
        'selected_date' : selected_date,
        'selected_date_sales' : selected_date_sales,
        'total_daily_sales' : total_daily_sales,
    }
    return render(request, 'pos/sales.html', context)

@login_required
def sale_datail_view(request, sale_id):
    sale_detail = get_object_or_404 (Sale, id=sale_id)
    return render(request, 'pos/sale-detail.html',{'sale' : sale_detail})

@login_required
def new_sale_view(request):
    form = SaleItemForm()
    user = request.user
    store = request.user.store
    payment_methods = PaymentMethod.objects.all()
    inventory_items = Item.objects.all()

    if request.method == 'POST':
        payments_data = request.POST.get('payments-data')
        payments_data = json.loads(payments_data)

        sale = Sale.objects.create(user=user, store=store)
        form = SaleItemForm(request.POST)

        product_ids = request.POST.get('product_ids')
        product_prices = request.POST.get('product_prices')
        quantities = request.POST.get('quantities')

        product_ids = product_ids.split(',')
        product_prices = product_prices.split(',')
        quantities = quantities.split(',')

        for method, value in payments_data.items():
            method = PaymentMethod.objects.get(id=method)
            Payment.objects.create(
                sale = sale,
                method=method,
                value=value,
            )

        for index in range(len(product_ids)):
            id = Product.objects.get(pk=product_ids[index])
            SaleItem.objects.create(
                sale = sale,
                product = id,
                price = float(product_prices[index]),
                quantity = int(quantities[index]),
            )
            inventory_item = Item.objects.filter(product=id, location=store).first()

            if inventory_item:
                inventory_item.quantity -= int(quantities[index])
                print(inventory_item.product, inventory_item.quantity, inventory_item.location)
            else:
                Item.objects.create(
                    product = id,
                    quantity = 0 - int(quantities[index]),
                    location = store
                )
                print(f'{id} criado')

            try:
                inventory_item.save()
            except:
                print('não salvo!')

        sale.save()

    context = {
        'form' : form,
        'payment_methods' : payment_methods,
        'inventory_items' : inventory_items,
    }
    return render(request, 'pos/new-sale.html', context)

@login_required
def exchange_view(request):
    sales = Sale.objects.all()

    if request.method == 'POST':
        exchange_inovice_id = request.POST.get('exchange_inovice_id')
        exchange_sale = Sale.objects.get(id=exchange_inovice_id)
        exchange_url = reverse('sale-detail', args=[exchange_inovice_id])
        return redirect(exchange_url)
    
    return render(request, 'pos/exchange.html', {})

@login_required
def add_payment_methods (request):
    payment_methods = PaymentMethod.objects.all()

    if request.method == 'POST':
        method = request.POST.get('new-method')
        new_method = PaymentMethod(name = method)
        new_method.save()

        print(method)

    return render(request, 'pos/payments.html', {'payment_methods' : payment_methods})