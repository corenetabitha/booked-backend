from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from orders_api.models import Order, OrderItem
from books_api.models import Book
from django.db import transaction
from django.shortcuts import get_object_or_404

class MpesaCheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        phone_number = request.data.get('phone')
        amount = request.data.get('amount')
        cart_items_data = request.data.get('cart_items')

        if not phone_number or not amount or not cart_items_data:
            return Response({"detail": "Phone number, amount, and cart items are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive.")
        except (ValueError, TypeError):
            return Response({"detail": "Invalid amount."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        try:
            print(f"Initiating M-Pesa STK push for {phone_number} with amount {amount}")

            with transaction.atomic():
                order = Order.objects.create(
                    user=user,
                    total_amount=amount,
                    status='Pending'
                )

                for item_data in cart_items_data:
                    book_id = item_data.get('book_id')
                    quantity = item_data.get('quantity', 1)

                    book = get_object_or_404(Book, id=book_id, is_available_for_purchase=True)

                    if book.stock_count < quantity:
                        raise ValueError(f"Not enough stock for '{book.title}'. Available: {book.stock_count}, Requested: {quantity}")

                    OrderItem.objects.create(
                        order=order,
                        book=book,
                        quantity=quantity,
                        price_at_purchase=book.price
                    )
                    book.stock_count -= quantity
                    book.save()

                order.status = 'Approved'
                order.save()

            return Response(
                {"message": "M-Pesa payment initiated and order created successfully (simulation). Please complete payment on your phone.",
                 "order_id": order.id},
                status=status.HTTP_200_OK
            )

        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"M-Pesa initiation failed: {e}")
            return Response({"detail": "Failed to initiate M-Pesa payment. Please try again later."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
