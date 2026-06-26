from django.http import HttpResponse
from django.db.models import Q, Count

from books.models import Book, Category


def books_view(request):
    books = Book.objects.filter(stock__gt=1).filter(
        Q(title__icontains="1943") |
        Q(author__icontains="taras")
    )

    result = ""

    for book in books:
        result += f"{book.title} - {book.author}<br>"

    return HttpResponse(result)


def categories_view(request):
    categories = Category.objects.annotate(books_count=Count("book"))

    result = ""

    for category in categories:
        result += f"{category.name}: {category.books_count}<br>"

    return HttpResponse(result)