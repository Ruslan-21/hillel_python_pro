from django.urls import path

from .views import (
    BooksListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    categories_view,
    async_books_view,
    async_categories_view,
    async_book_detail_view,
)


app_name = "books"

urlpatterns = [
    path("", BooksListView.as_view(), name="list"),
    path("create/", BookCreateView.as_view(), name="book_create"),

    path("async/", async_books_view, name="async_books"),
    path(
        "async-categories/",
        async_categories_view,
        name="async_categories",
    ),
    path(
        "async-book/<int:pk>/",
        async_book_detail_view,
        name="async_book_detail",
    ),

    path("<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("<int:pk>/update/", BookUpdateView.as_view(), name="book_update"),
    path("<int:pk>/delete/", BookDeleteView.as_view(), name="book_delete"),
    path("categories/", categories_view, name="categories"),
]