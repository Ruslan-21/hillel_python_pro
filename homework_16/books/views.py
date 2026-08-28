from django.http import HttpResponse
from django.db.models import Q, Count
from cart.forms import CartAddBookForm
from books.models import Book, Category
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import BookSerializer, CategorySerializer


def books_view(request):
    books = Book.objects.filter(stock__gt=1).filter(
        Q(title__icontains="1943") |
        Q(author__icontains="taras")
    )

    result = ""

    for book in books:
        result += f"{book.title} - {book.author}<br>"

    return HttpResponse(result)


async def async_books_view(request):
    books = Book.objects.all()

    result = ""

    async for book in books:
        result += f"{book.title} - {book.author}<br>"

    if not result:
        result = "No books found"

    return HttpResponse(result)


def categories_view(request):
    categories = Category.objects.annotate(
        books_count=Count("book")
    )

    result = ""

    for category in categories:
        result += f"{category.name}: {category.books_count}<br>"

    return HttpResponse(result)


async def async_categories_view(request):
    categories = Category.objects.annotate(
        books_count=Count("book")
    )

    result = ""

    async for category in categories:
        result += f"{category.name}: {category.books_count}<br>"

    if not result:
        result = "No categories found"

    return HttpResponse(result)


async def async_book_detail_view(request, pk):
    try:
        book = await Book.objects.aget(pk=pk)
        result = f"{book.title} - {book.author}"
    except Book.DoesNotExist:
        result = "Book not found"

    return HttpResponse(result)


class BooksListView(ListView):
    model = Book
    paginate_by = 5
    ordering = ["id"]

    def get_queryset(self):
        query = self.request.GET.get("q")

        queryset = Book.objects.all()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query)
            )

        return queryset.order_by("id")


class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_book_form"] = CartAddBookForm()
        return context


class BookCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "books.add_book"
    raise_exception = True

    model = Book
    fields = "__all__"
    success_url = reverse_lazy("books:list")


class BookUpdateView(UpdateView):
    model = Book
    fields = "__all__"
    success_url = reverse_lazy("books:list")


class BookDeleteView(DeleteView):
    model = Book
    template_name = "books/book_confirm_delete.html"
    success_url = reverse_lazy("books:list")



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("category").all()
    serializer_class = BookSerializer

    filterset_fields = ["category", "author"]
    search_fields = ["title", "author", "description"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]