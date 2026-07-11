from django.http import HttpResponse
from django.db.models import Q, Count

from books.models import Book, Category
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView



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



class BooksListView(ListView):
    model = Book
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get("q")

        if query:
            return Book.objects.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query)
            )
        return Book.objects.all()


class BookDetailView(DetailView):
    model = Book


class BookCreateView(CreateView):
    model = Book
    fields = "__all__"
    success_url = reverse_lazy("books:books")


class BookUpdateView(UpdateView):
    model = Book
    fields = "__all__"
    success_url = reverse_lazy("books:books")


class BookDeleteView(DeleteView):
    model = Book
    template_name = "books/book_confirm_delete.html"
    success_url = reverse_lazy("books:books")