import pytest
from unittest.mock import patch

from django.urls import reverse

from orders.models import Order, OrderItem
from tests.factories import BookFactory
from cart.cart import Cart


@pytest.mark.django_db
def test_order_create_get(client):
    response = client.get(reverse("orders:order_create"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_order_create_empty_cart(client):
    response = client.post(
        reverse("orders:order_create"),
        data={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "address": "Main Street 1",
            "city": "Dnipro",
            "postal_code": "49000",
        },
    )

    assert response.status_code == 200
    assert Order.objects.count() == 1


@pytest.mark.django_db
@patch("orders.views.send_mail")
def test_order_create_sends_email(mock_send_mail, client):
    book = BookFactory(price="20.00")

    session = client.session
    session["cart"] = {
        str(book.id): {
            "quantity": 1,
            "price": "20.00",
        }
    }
    session.save()

    response = client.post(
        reverse("orders:order_create"),
        data={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "address": "Main Street 1",
            "city": "Dnipro",
            "postal_code": "49000",
        },
    )

    assert response.status_code == 200
    assert Order.objects.count() == 1
    mock_send_mail.assert_called_once()


@pytest.mark.django_db
def test_order_model_creation():
    order = Order.objects.create(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        address="Main Street 1",
        city="Dnipro",
        postal_code="49000",
    )

    assert order.pk is not None
    assert order.first_name == "John"
    assert order.email == "john@example.com"


@pytest.mark.django_db
def test_order_item_creation():
    book = BookFactory(price="25.00")

    order = Order.objects.create(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        address="Main Street 1",
        city="Dnipro",
        postal_code="49000",
    )

    item = OrderItem.objects.create(
        order=order,
        book=book,
        price="25.00",
        quantity=2,
    )

    assert item.pk is not None
    assert item.order == order
    assert item.book == book
    assert item.quantity == 2


@pytest.mark.django_db
def test_payment_success(client):
    response = client.get(reverse("orders:payment_success"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_payment_cancel(client):
    response = client.get(reverse("orders:payment_cancel"))

    assert response.status_code == 200


@pytest.mark.django_db
@patch("orders.views.stripe.checkout.Session.create")
def test_create_checkout_session(mock_stripe, client):
    book = BookFactory(price="25.00")

    order = Order.objects.create(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        address="Main Street 1",
        city="Dnipro",
        postal_code="49000",
    )

    OrderItem.objects.create(
        order=order,
        book=book,
        price="25.00",
        quantity=2,
    )

    mock_stripe.return_value.url = "https://checkout.stripe.com/test-session"

    response = client.get(
        reverse(
            "orders:create_checkout_session",
            kwargs={"order_id": order.id},
        )
    )

    assert response.status_code == 302
    assert response.url == "https://checkout.stripe.com/test-session"

    mock_stripe.assert_called_once()

    call_kwargs = mock_stripe.call_args.kwargs

    assert call_kwargs["mode"] == "payment"
    assert call_kwargs["payment_method_types"] == ["card"]
    assert len(call_kwargs["line_items"]) == 1
    assert call_kwargs["line_items"][0]["quantity"] == 2
