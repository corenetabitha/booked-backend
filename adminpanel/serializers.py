from rest_framework import serializers
from .models import Book, Order, LendingRequest

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class LendingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LendingRequest
        fields = '__all__'
