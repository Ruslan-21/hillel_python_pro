import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from tests.factories import BookFactory, CategoryFactory
from orders.models import Order


User = get_user_model()


@pytest.mark.django_db
def test_user_registration_flow(client):
    response = client.post(
        reverse("register"),
        {
            "username": "integration_user",
            "email": "integration@example.com",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("login")

    user = User.objects.get(username="integration_user")

    assert user.email == "integration@example.com"
    assert user.check_password("StrongPassword123!")


@pytest.mark.django_db
def test_user_registration_invalid_password_flow(client):
    response = client.post(
        reverse("register"),
        {
            "username": "integration_user",
            "email": "integration@example.com",
            "password1": "StrongPassword123!",
            "password2": "WrongPassword123!",
        },
    )

    assert response.status_code == 200

    assert not User.objects.filter(
        username="integration_user"
    ).exists()


@pytest.mark.django_db
def test_user_login_flow(client):
    user = User.objects.create_user(
        username="login_user",
        email="login@example.com",
        password="StrongPassword123!",
    )

    response = client.post(
        reverse("login"),
        {
            "username": "login_user",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 302
    assert response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_user_login_invalid_password_flow(client):
    User.objects.create_user(
        username="login_user",
        email="login@example.com",
        password="StrongPassword123!",
    )

    response = client.post(
        reverse("login"),
        {
            "username": "login_user",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 200
    assert not response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_books_browsing_flow(client):
    book = BookFactory(title="Integration Book")

    response = client.get(reverse("books:list"))

    assert response.status_code == 200
    assert "Integration Book" in response.content.decode()

    response = client.get(
        reverse(
            "books:book_detail",
            kwargs={"pk": book.pk},
        )
    )

    assert response.status_code == 200
    assert "Integration Book" in response.content.decode()


@pytest.mark.django_db
def test_books_search_flow(client):
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
def test_category_books_flow(client):
    category = CategoryFactory(name="Fantasy")

    BookFactory(
        title="Fantasy Book One",
        category=category,
    )
    BookFactory(
        title="Fantasy Book Two",
        category=category,
    )

    response = client.get(reverse("books:categories"))

    assert response.status_code == 200

    content = response.content.decode()

    assert "Fantasy: 2" in content


@pytest.mark.django_db
def test_async_books_flow(client):
    BookFactory(title="Async Integration Book")

    response = client.get(
        reverse("books:async_books")
    )

    assert response.status_code == 200
    assert "Async Integration Book" in response.content.decode()


@pytest.mark.django_db
def test_async_categories_flow(client):
    category = CategoryFactory(name="Science")

    BookFactory(category=category)

    response = client.get(
        reverse("books:async_categories")
    )

    assert response.status_code == 200
    assert "Science: 1" in response.content.decode()


@pytest.mark.django_db
def test_async_book_detail_flow(client):
    book = BookFactory(
        title="Integration Async Book",
        author="Integration Author",
    )

    response = client.get(
        reverse(
            "books:async_book_detail",
            kwargs={"pk": book.pk},
        )
    )

    assert response.status_code == 200

    content = response.content.decode()

    assert "Integration Async Book" in content
    assert "Integration Author" in content


@pytest.mark.django_db
def test_async_book_detail_not_found_flow(client):
    response = client.get(
        reverse(
            "books:async_book_detail",
            kwargs={"pk": 99999},
        )
    )

    assert response.status_code == 200
    assert "Book not found" in response.content.decode()


@pytest.mark.django_db
def test_order_creation_flow(client):
    book = BookFactory(
        title="Integration Order Book",
        price="25.00",
    )

    client.session["cart"] = {
        str(book.id): {
            "quantity": 2,
            "price": "25.00",
        }
    }
    client.session.save()

    response = client.post(
        reverse("orders:order_create"),
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "address": "Main Street 1",
            "city": "Dnipro",
            "postal_code": "49000",
        },
    )

    assert response.status_code == 200

    content = response.content.decode()

    assert "Thank you for your order!" in content
    assert "Your order" in content

    order = Order.objects.get(
        email="john@example.com"
    )

    assert order.first_name == "John"
    assert order.last_name == "Doe"
    assert order.city == "Dnipro"


@pytest.mark.django_db
def test_order_create_get_flow(client):
    response = client.get(
        reverse("orders:order_create")
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_cart_add_flow(client):
    book = BookFactory(
        title="Integration Cart Book",
        price="30.00",
    )

    response = client.post(
        reverse(
            "cart:cart_add",
            kwargs={"book_id": book.id},
        ),
        {
            "quantity": 2,
        },
    )

    assert response.status_code == 302

    session = client.session
    cart = session.get("cart")

    assert str(book.id) in cart
    assert cart[str(book.id)]["quantity"] == 2


@pytest.mark.django_db
def test_cart_remove_flow(client):
    book = BookFactory(
        title="Integration Remove Book",
        price="20.00",
    )

    client.session["cart"] = {
        str(book.id): {
            "quantity": 1,
            "price": "20.00",
        }
    }
    client.session.save()

    response = client.post(
        reverse(
            "cart:cart_remove",
            kwargs={"book_id": book.id},
        )
    )

    assert response.status_code == 302

    session = client.session
    cart = session.get("cart", {})

    assert str(book.id) not in cart


@pytest.mark.django_db
def test_cart_detail_flow(client):
    book = BookFactory(
        title="Integration Cart Detail Book",
        price="15.00",
    )

    response = client.post(
        reverse(
            "cart:cart_add",
            kwargs={"book_id": book.id},
        ),
        {
            "quantity": 3,
        },
    )

    assert response.status_code == 302

    response = client.get(
        reverse("cart:cart_detail")
    )

    assert response.status_code == 200

    content = response.content.decode()

    assert "Integration Cart Detail Book" in content