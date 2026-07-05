from django.urls import path
from .views import BooksListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView, categories_view



app_name = "books"

urlpatterns = [

    path("", BooksListView.as_view(), name="books"),
    path("create/", BookCreateView.as_view(), name="book_create"),
    path("<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("<int:pk>/update/", BookUpdateView.as_view(), name="book_update"),
    path("<int:pk>/delete/", BookDeleteView.as_view(), name="book_delete"),
    path("categories/", categories_view, name="categories"),
]