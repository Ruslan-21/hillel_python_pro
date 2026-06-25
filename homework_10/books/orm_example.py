from django.db.models import Q, Count
from homework_10.books.models import Book, Category


Book.objects.filter(stock__gt=1)

Book.objects.filter(
    Q(title__icontains="1943")|
    Q(author__icontains="taras")
)

categories = Category.objects.annotate(
    books_count=Count("book")
)
for category in categories:
    print(category.name, category.books_count)