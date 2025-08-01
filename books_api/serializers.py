from rest_framework import serializers
from .models import Book, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    genre_name = serializers.CharField(source='genre.name', read_only=True)
    genre = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), write_only=True, allow_null=True, required=False
    ) 

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'description', 'price', 'genre', 'genre_name', 
            'image_url', 'stock_count', 'is_available_for_purchase',
            'is_available_for_lending', 'created_at', 'updated_at'
        ]

    def validate(self, data):
        is_for_purchase = data.get('is_available_for_purchase', False)
        is_for_lending = data.get('is_available_for_lending', False)

        if is_for_purchase and is_for_lending:
            raise serializers.ValidationError("A book cannot be available for both purchase and lending simultaneously.")
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.genre:
            representation['genre'] = GenreSerializer(instance.genre).data
        return representation