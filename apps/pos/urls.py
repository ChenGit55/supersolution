from django.urls import path, include
from .views import sales_view, new_sale_view, SaleList, SaleViewSet, SaleItemList, SaleItemViewSet, add_payment_methods, sale_datail_view, exchange_view
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'sales', SaleViewSet)
router.register(r'sales-items', SaleItemViewSet)

urlpatterns = [
    path('', sales_view, name='sales'),
    path('new/', new_sale_view, name='new-sale'),
    path('sales/', SaleList.as_view(), name='api-sales'),
    path("detail/<int:sale_id>", sale_datail_view, name="sale-detail"),
    path("exchange/", exchange_view, name="exchange"),
    path('sales-items/', SaleItemList.as_view(), name='api-sales-items'),
    path('api/', include(router.urls)),
    path('add-payment-methods', add_payment_methods, name='add-payment-methods' ),
]