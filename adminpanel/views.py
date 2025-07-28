from django.shortcuts import render
from rest_framework import viewsets
from .models import Book, Order, LendingRequest
from .serializers import BookSerializer, OrderSerializer, LendingRequestSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class LendingRequestViewSet(viewsets.ModelViewSet):
    queryset = LendingRequest.objects.all()
    serializer_class = LendingRequestSerializer
