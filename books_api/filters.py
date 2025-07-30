import django_filters
from .models import Book 

class BookFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')

    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')

    genre = django_filters.CharFilter(field_name='genre__name', lookup_expr='iexact')

    class Meta:
        model = Book
        fields = [
            'is_available_for_purchase',
            'is_available_for_lending',
        ]
