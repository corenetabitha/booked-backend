from django.urls import path
from .views import MpesaCheckoutView

urlpatterns = [
    path('cart/mpesa/checkout/', MpesaCheckoutView.as_view(), name='mpesa_checkout'),
]