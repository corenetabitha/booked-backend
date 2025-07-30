from rest_framework import serializers
from .models import Lending
from books_api.models import Book
from users_api.serializers import UserProfileSerializer

class LendingSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True)
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Lending
        fields = ['id', 'user', 'book', 'book_id', 'lending_date', 'due_date', 'returned_date']
        read_only_fields = ['id', 'user', 'book', 'lending_date']

    def create(self, validated_data):
        book = validated_data.get('book_id')
        due_date = validated_data.get('due_date')

        if not book:
            raise serializers.ValidationError({"book_id": "This field is required."})

        lending = Lending.objects.create(
            user=self.context['request'].user,
            book=book,
            due_date=due_date
        )
        return lending

class ReturnRequestSerializer(serializers.Serializer):
    lending_id = serializers.IntegerField()
    returned = serializers.BooleanField()

    def validate_lending_id(self, value):
        if not Lending.objects.filter(id=value).exists():
            raise serializers.ValidationError("Lending with this ID does not exist.")
        return value

