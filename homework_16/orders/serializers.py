from rest_framework import serializers

from books.models import Book
from books.serializers import BookSerializer

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        source="book",
        write_only=True,
    )

    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "book",
            "book_id",
            "price",
            "quantity",
            "total_cost",
        ]
        read_only_fields = [
            "price",
            "total_cost",
        ]

    def get_total_cost(self, obj):
        return obj.get_cost()


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "city",
            "postal_code",
            "created",
            "updated",
            "paid",
            "items",
        ]
        read_only_fields = [
            "id",
            "created",
            "updated",
            "paid",
            "items",
        ]