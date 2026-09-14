import pytest
from django.urls import reverse

from tests.factories import BookFactory, CategoryFactory


@pytest.mark.django_db
def test_books_list_view(client):
    BookFactory(title="Book One")
    BookFactory(title="Book Two")

    response = client.get(reverse("books:list"))

    assert response.status_code == 200
    assert "Book One" in response.content.decode()
    assert "Book Two" in response.content.decode()


@pytest.mark.django_db
def test_books_list_view_empty(client):
    response = client.get(reverse("books:list"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_books_list_search(client):
    BookFactory(title="Python Django")
    BookFactory(title="Harry Potter")

    response = client.get(
        reverse("books:list"),
        {"q": "Python"},
    )

    assert response.status_code == 200
    content = response.content.decode()

    assert "Python Django" in content
    assert "Harry Potter" not in content


@pytest.mark.django_db
def test_book_detail_view(client):
    book = BookFactory(title="The Hobbit")

    response = client.get(
        reverse("books:book_detail", kwargs={"pk": book.pk})
    )

    assert response.status_code == 200
    assert "The Hobbit" in response.content.decode()


@pytest.mark.django_db
def test_book_detail_view_404(client):
    response = client.get(
        reverse("books:book_detail", kwargs={"pk": 99999})
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_categories_view(client):
    category = CategoryFactory(name="Fantasy")
    BookFactory(category=category)
    BookFactory(category=category)

    response = client.get(reverse("books:categories"))

    assert response.status_code == 200
    assert "Fantasy: 2" in response.content.decode()


@pytest.mark.django_db
def test_async_books_view(client):
    BookFactory(title="Async Book")

    response = client.get(reverse("books:async_books"))

    assert response.status_code == 200
    assert "Async Book" in response.content.decode()


@pytest.mark.django_db
def test_async_categories_view(client):
    category = CategoryFactory(name="Science")
    BookFactory(category=category)

    response = client.get(reverse("books:async_categories"))

    assert response.status_code == 200
    assert "Science: 1" in response.content.decode()


@pytest.mark.django_db
def test_async_book_detail_view(client):
    book = BookFactory(
        title="Async Detail Book",
        author="Test Author",
    )

    response = client.get(
        reverse(
            "books:async_book_detail",
            kwargs={"pk": book.pk},
        )
    )

    assert response.status_code == 200

    content = response.content.decode()

    assert "Async Detail Book" in content
    assert "Test Author" in content


@pytest.mark.django_db
def test_async_book_detail_view_not_found(client):
    response = client.get(
        reverse(
            "books:async_book_detail",
            kwargs={"pk": 99999},
        )
    )

    assert response.status_code == 200
    assert "Book not found" in response.content.decode()
