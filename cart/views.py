from rest_framework import viewsets
from .models import CartItem, Book
from .serializers import CartItemSerializer, BookSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .mpesa import simulate_payment

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        cart_item = self.get_object()
        amount = cart_item.book.price * cart_item.quantity
        simulate_payment(amount)
        return Response({"status": "Payment initiated"})

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

