from rest_framework import serializers
from .models import Order, OrderItem
from books_api.models import Book
from users_api.serializers import UserProfileSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'book', 'book_title', 'book_id', 'quantity', 'price_at_purchase',]
        read_only_fields = ['id', 'order', 'book', 'price_at_purchase',]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = UserProfileSerializer(read_only=True) 
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    items = OrderItemSerializer(source='order_items', many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'user_id', 'order_date', 'total_amount', 'status', 'items']
        read_only_fields = ['id', 'user', 'order_date', 'total_amount', 'status']

    def create(self, validated_data):
        order_items_data = validated_data.pop('items')
        user = self.context['request'].user

        total = 0  
        for item_data in order_items_data:
            book = item_data['book_id']
            quantity = item_data['quantity']
            total += book.price * quantity

        
        order = Order.objects.create(user=user, total_amount=total, **validated_data)

        for item_data in order_items_data:
            book = item_data['book_id']
            quantity = item_data['quantity']
            OrderItem.objects.create(
                order=order,
                book=book,
                quantity=quantity,
                price_at_purchase=book.price
            )

        return order