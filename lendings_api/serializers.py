from rest_framework import serializers
from django.utils import timezone
from .models import Lending
from books_api.models import Book
from users_api.serializers import UserProfileSerializer


class LendingSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True)
    user = UserProfileSerializer(read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Lending
        fields = ['id', 'user', 'book', 'book_title', 'book_id', 'lending_date', 'due_date', 'returned_date', 'status']
        read_only_fields = ['id', 'user', 'book', 'lending_date', 'status']

    def create(self, validated_data):
        request_user = self.context['request'].user
        book = validated_data.get('book_id')
        due_date = validated_data.get('due_date')

        
        if Lending.objects.filter(user=request_user, book=book, status__in=['pending', 'borrowed']).exists():
            raise serializers.ValidationError(
                "You already have an active lending request or borrowed this book."
            )

        lending = Lending.objects.create(
            user=request_user,
            book=book,
            due_date=due_date,
            status='pending'  
        )
        return lending


class ReturnRequestSerializer(serializers.Serializer):
    lending_id = serializers.IntegerField()
    returned = serializers.BooleanField()

    def validate_lending_id(self, value):
        try:
            lending = Lending.objects.get(id=value)
        except Lending.DoesNotExist:
            raise serializers.ValidationError("Lending with this ID does not exist.")
        return value

    def update(self, instance, validated_data):
        if validated_data['returned']:
            instance.returned_date = timezone.now()
            instance.status = 'returned'
        else:
            instance.returned_date = None  
        instance.save()
        return instance

