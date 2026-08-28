from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from books.models import Book
from .cart import Cart


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        cart = Cart(request)

        items = []

        for item in cart:
            items.append({
                "book_id": item["book"].id,
                "title": item["book"].title,
                "price": str(item["price"]),
                "quantity": item["quantity"],
                "total_price": str(item["total_price"]),
            })

        return Response({
            "items": items,
            "total_price": str(cart.get_total_price()),
            "total_quantity": len(cart),
        })

    def create(self, request):
        book_id = request.data.get("book_id")
        quantity = request.data.get("quantity", 1)
        update_quantity = request.data.get("update_quantity", False)

        if not book_id:
            return Response(
                {"detail": "book_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"detail": "Book not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response(
                {"detail": "quantity must be an integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity < 1:
            return Response(
                {"detail": "quantity must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = Cart(request)

        cart.add(
            book=book,
            quantity=quantity,
            update_quantity=update_quantity,
        )

        return Response(
            {"detail": "Book added to cart"},
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, pk=None):
        try:
            book = Book.objects.get(id=pk)
        except Book.DoesNotExist:
            return Response(
                {"detail": "Book not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart = Cart(request)
        cart.remove(book)

        return Response(status=status.HTTP_204_NO_CONTENT)
