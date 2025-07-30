from rest_framework import serializers
from .models import Order, OrderItem
from books_api.models import Book 
from books_api.serializers import BookSerializer 


class OrderItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True) 

    class Meta:
        model = OrderItem
        fields = ['id', 'book', 'book_id', 'quantity', 'price_at_purchase']
        read_only_fields = ['price_at_purchase'] 

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True) 
    
    book_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False,
        help_text="List of book IDs to include in the order."
    )

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_date', 'total_amount', 'status', 'items', 'book_ids']
        read_only_fields = ['user', 'order_date', 'total_amount', 'status']

    def create(self, validated_data):
        book_ids = validated_data.pop('book_ids', [])
        user = self.context['request'].user
        if not user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to create an order.")

        order = Order.objects.create(user=user, total_amount=0, **validated_data)

        calculated_total = 0
        order_items = []
        for book_id in book_ids:
            try:
                book = Book.objects.get(id=book_id, is_available_for_purchase=True, stock_count__gt=0)
                
                if book.stock_count < 1:
                    raise serializers.ValidationError(f"Book '{book.title}' is out of stock.")

                order_item = OrderItem(
                    order=order,
                    book=book,
                    quantity=1, 
                    price_at_purchase=book.price
                )
                order_items.append(order_item)
                calculated_total += book.price
                book.stock_count -= 1 
                book.save()
            except Book.DoesNotExist:
                order.delete()
                raise serializers.ValidationError(f"Book with ID {book_id} not found or not available for purchase.")

        OrderItem.objects.bulk_create(order_items)
        order.total_amount = calculated_total
        order.save()
        return order

    def update(self, instance, validated_data):
        if 'status' in validated_data:
            instance.status = validated_data['status']
            instance.save()
            return instance
        raise serializers.ValidationError("Only order status can be updated.")