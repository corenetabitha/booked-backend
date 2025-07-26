# /home/corene/project-backend/backend/api/serializers.py

from rest_framework import serializers
from .models import Book, Genre
from django.contrib.auth.models import User # Make sure User is imported

# NEW: Genre Serializer
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    # OPTIONAL: To display the genre name instead of just its ID in the Book API response
    genre_name = serializers.StringRelatedField(source='genre', read_only=True)

    class Meta:
        model = Book
        fields = '__all__'
        # If you use genre_name, you can make it read-only if you also have 'genre' in fields
        read_only_fields = ['genre_name']

# RESTORED/CONFIRMED: User Serializer for registration and login
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}} # Password should only be written, not read back

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user