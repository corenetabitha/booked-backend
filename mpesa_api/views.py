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
        data = request.data
        phone_number = data.get('phone')
        amount = data.get('amount')
        cart_items_data = data.get('cart_items')

        if not phone_number or not amount or not cart_items_data:
            return Response(
                {"detail": "Phone, amount, and cart items are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            amount = float(amount)
            if amount <= 0:
                return Response({"detail": "Amount must be a positive number."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"detail": "Invalid amount format."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=user,
                    total_amount=amount,
                    status='Pending'
                )

                for item in cart_items_data:
                    book_id = item.get('book_id')
                    quantity = item.get('quantity', 1)

                    if not book_id:
                        raise ValueError("Missing book_id in cart item.")

                    book = get_object_or_404(Book, id=book_id, is_available_for_purchase=True)

                    try:
                        quantity = int(quantity)
                        if quantity <= 0:
                            raise ValueError()
                    except:
                        raise ValueError(f"Invalid quantity for '{book.title}'.")

                    if book.stock_count < quantity:
                        raise ValueError(f"Not enough stock for '{book.title}'.")

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
                {"message": "Payment prompt sent. Order created successfully.", "order_id": order.id},
                status=status.HTTP_201_CREATED
            )

        except ValueError as ve:
            return Response({"detail": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"detail": "Something went wrong. Try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
