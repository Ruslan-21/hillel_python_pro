import pytest
from decimal import Decimal

from books.models import Book, Category
from tests.factories import BookFactory, CategoryFactory


@pytest.mark.django_db
def test_category_creation():
    category = CategoryFactory()

    assert category.pk is not None
    assert category.name.startswith("Category")
    assert category.slug.startswith("category-")


@pytest.mark.django_db
def test_category_str():
    category = CategoryFactory(name="Fantasy")

    assert str(category) == "Fantasy"


@pytest.mark.django_db
def test_category_name():
    category = CategoryFactory(name="Science Fiction")

    assert category.name == "Science Fiction"


@pytest.mark.django_db
def test_category_slug_unique():
    CategoryFactory(slug="unique-category")

    with pytest.raises(Exception):
        CategoryFactory(slug="unique-category")


@pytest.mark.django_db
def test_book_creation():
    book = BookFactory()

    assert book.pk is not None
    assert book.title.startswith("Book")
    assert book.author.startswith("Author")


@pytest.mark.django_db
def test_book_str():
    book = BookFactory(title="The Hobbit")

    assert str(book) == "The Hobbit"


@pytest.mark.django_db
def test_book_price():
    book = BookFactory(price=Decimal("19.99"))

    book.refresh_from_db()

    assert book.price == Decimal("19.99")


@pytest.mark.django_db
def test_book_stock():
    book = BookFactory(stock=10)

    assert book.stock == 10


@pytest.mark.django_db
def test_book_description_can_be_empty():
    book = BookFactory(description="")

    assert book.description == ""


@pytest.mark.django_db
def test_book_category_relation():
    category = CategoryFactory(name="Fantasy")
    book = BookFactory(category=category)

    assert book.category == category
    assert book.category.name == "Fantasy"


@pytest.mark.django_db
def test_book_without_category():
    book = BookFactory(category=None)

    assert book.category is None


@pytest.mark.django_db
def test_category_can_have_books():
    category = CategoryFactory()

    BookFactory(category=category)
    BookFactory(category=category)

    assert category.book_set.count() == 2


@pytest.mark.django_db
def test_category_slug_value():
    category = CategoryFactory(
        name="Programming",
        slug="programming",
    )

    assert category.name == "Programming"
    assert category.slug == "programming"


@pytest.mark.django_db
def test_book_author_and_title():
    book = BookFactory(
        title="Clean Code",
        author="Robert Martin",
    )

    assert book.title == "Clean Code"
    assert book.author == "Robert Martin"


@pytest.mark.django_db
def test_book_price_and_stock():
    book = BookFactory(
        price=Decimal("29.99"),
        stock=15,
    )

    assert book.price == Decimal("29.99")
    assert book.stock == 15