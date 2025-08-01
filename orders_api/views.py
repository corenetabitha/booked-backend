from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.decorators import action

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == 'admin':
            return Order.objects.all().order_by('-order_date')
        return Order.objects.filter(user=self.request.user).order_by('-order_date')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.role != 'admin':
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        if 'status' in request.data:
            serializer = self.get_serializer(instance, data={'status': request.data['status']}, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response({"detail": "Only 'status' field can be updated."},
                        status=status.HTTP_400_BAD_REQUEST)

    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        order = self.get_object()
        if request.user.role != 'admin':
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        order.status = 'Approved'
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        order = self.get_object()
        if request.user.role != 'admin':
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        order.status = 'Rejected'
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)
