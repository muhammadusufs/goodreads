from rest_framework.serializers import ModelSerializer
from books.models import Book, BookReview
from users.models import CustomUser
from rest_framework import serializers


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'isbn']

class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']

class BookReviewSerializer(ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BookReview
        fields = ['user', 'book', 'comment', 'stars_given', 'user_id', 'book_id']