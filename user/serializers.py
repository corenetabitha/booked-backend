from rest_framework import serializers
from .models import Order, Lending

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status', 'total', 'created_at']


class LendingSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Lending
        fields = ['id', 'book_title', 'status', 'due_date', 'returned']
