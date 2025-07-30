from rest_framework import serializers
from .models import Lending
from books_api.models import Book

from books_api.serializers import BookSerializer
from users_api.serializers import UserProfileSerializer

class LendingSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    book = BookSerializer(read_only=True)
    user = UserProfileSerializer(read_only=True)

    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), write_only=True, required=True
    )

    class Meta:
        model = Lending
        fields = [
            'id', 'user', 'user_id', 'book', 'book_id', 'book_title',
            'lending_date', 'due_date', 'returned_date', 'status'
        ]
        read_only_fields = ['user', 'lending_date', 'due_date', 'returned_date']

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to request a lending.")

        book = validated_data['book']
        if not book.is_available_for_lending:
            raise serializers.ValidationError(f"Book '{book.title}' is not available for lending.")

        if Lending.objects.filter(user=user, book=book, status__in=['Pending', 'Approved', 'Lent']).exists():
            raise serializers.ValidationError("You already have an active lending request or an active lending for this book.")

        lending = Lending.objects.create(user=user, **validated_data)
        return lending

    def update(self, instance, validated_data):
        if 'status' in validated_data:
            instance.status = validated_data['status']
            if instance.status == 'Returned' and not instance.returned_date:
                instance.returned_date = date.today()
        return super().update(instance, validated_data)

class ReturnRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255, required=False)
