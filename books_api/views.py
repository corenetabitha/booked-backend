from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book, Genre
from .serializers import BookSerializer, GenreSerializer
from .filters import BookFilter

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAdminUser | permissions.IsAuthenticatedOrReadOnly]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author', 'description']
    ordering_fields = ['title', 'author', 'price', 'created_at']
    ordering = ['-created_at']
    pagination_class = None

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]

    def get_queryset(self):
        queryset = super().get_queryset()

        availability = self.request.query_params.get('availability', None)
        if availability == 'purchase':
            queryset = queryset.filter(is_available_for_purchase=True, stock_count__gt=0)
        elif availability == 'lending':
            queryset = queryset.filter(is_available_for_lending=True)

        return queryset
