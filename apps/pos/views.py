from django.shortcuts import render
from .models import Sale, SaleItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .serializers import SaleSerializer, SaleItemSerializer
from rest_framework import generics, viewsets
from rest_framework.decorators import permission_classes

class SaleList(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class SaleViewSet(LoginRequiredMixin  ,viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = Sale

@login_required
def sales_view(request):
    return render(request, 'pos/sales.html', {})

@login_required
def new_sale_view(request):
    user = request.user
    context = {
        user:'user',
    }
    return render(request, 'pos/new-sale.html', context)