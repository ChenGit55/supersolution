from django.shortcuts import render
from .models import Sale, SaleItem
from rest_framework import generics, viewsets
from .serializers import SaleSerializer, SaleItemSerializer

class SaleList(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = Sale

def sales_view(request):
    return render(request, 'pos/sales.html', {})

def new_sale_view(request):
    user = request.user
    context = {
        user:'user',
    }
    return render(request, 'pos/new-sale.html', context)