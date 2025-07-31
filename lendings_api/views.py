from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from .models import Lending
from .serializers import LendingSerializer, ReturnRequestSerializer
from django.shortcuts import get_object_or_404
from datetime import date

class LendingViewSet(viewsets.ModelViewSet):
    queryset = Lending.objects.all()
    serializer_class = LendingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == 'admin':
            return Lending.objects.all().order_by('-lending_date')
        return Lending.objects.filter(user=self.request.user).order_by('-lending_date')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.role != 'admin':
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.role != 'admin':
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_status(self, request, pk=None):
        lending = self.get_object()

        if request.user.role != 'admin':
            return Response({"detail": "Only admins can update lending status."}, status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get('status')
        if new_status not in ['Approved', 'Rejected']:
            return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        lending.status = new_status
        lending.save()
        return Response({"message": f"Lending request {new_status.lower()}."}, status=status.HTTP_200_OK)

class ReturnRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, lending_id):
        lending = get_object_or_404(Lending, id=lending_id, user=request.user)

        if lending.status != 'Lent':
            return Response(
                {"detail": "Book is not currently lent out or cannot be returned."},
                status=status.HTTP_400_BAD_REQUEST
            )

        lending.status = 'Returned'
        lending.returned_date = date.today()
        lending.save()

        return Response(
            {"message": f"Return request for '{lending.book.title}' submitted successfully. Status updated to Returned."},
            status=status.HTTP_200_OK
        )
