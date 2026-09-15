from django.contrib import admin
from .models import Book, Category
# Register your models here.


class BookInline(admin.TabularInline):
    model = Book
    extra = 1

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    search_fields = (
        "title",
        "author",
    )

    list_display = (
        "title",
        "author",
        "price",
        "stock",
        "category",
    )

    list_filter = (
        "category",
        "author",
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
    )

    inlines = [BookInline]