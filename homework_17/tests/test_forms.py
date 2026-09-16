import pytest

from cart.forms import CartAddBookForm
from orders.forms import OrderCreateForm
from users.forms import RegisterForm


def test_cart_form_valid():
    form = CartAddBookForm(data={
        "quantity": 2,
        "override": False,
    })

    assert form.is_valid()


def test_cart_form_quantity_required():
    form = CartAddBookForm(data={
        "override": False,
    })

    assert not form.is_valid()
    assert "quantity" in form.errors


def test_cart_form_quantity_minimum():
    form = CartAddBookForm(data={
        "quantity": 0,
        "override": False,
    })

    assert not form.is_valid()
    assert "quantity" in form.errors


def test_cart_form_quantity_positive():
    form = CartAddBookForm(data={
        "quantity": 1,
    })

    assert form.is_valid()


def test_cart_form_override_optional():
    form = CartAddBookForm(data={
        "quantity": 3,
    })

    assert form.is_valid()
    assert form.cleaned_data["override"] is False


def test_cart_form_override_true():
    form = CartAddBookForm(data={
        "quantity": 3,
        "override": True,
    })

    assert form.is_valid()
    assert form.cleaned_data["override"] is True


# =========================
# OrderCreateForm
# =========================

@pytest.mark.django_db
def test_order_form_valid():
    form = OrderCreateForm(data={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "address": "Main Street 1",
        "city": "Dnipro",
        "postal_code": "49000",
    })

    assert form.is_valid()


@pytest.mark.django_db
def test_order_form_required_fields():
    form = OrderCreateForm(data={})

    assert not form.is_valid()

    assert "first_name" in form.errors
    assert "last_name" in form.errors
    assert "email" in form.errors
    assert "address" in form.errors
    assert "city" in form.errors
    assert "postal_code" in form.errors


@pytest.mark.django_db
def test_order_form_invalid_email():
    form = OrderCreateForm(data={
        "first_name": "John",
        "last_name": "Doe",
        "email": "wrong-email",
        "address": "Main Street 1",
        "city": "Dnipro",
        "postal_code": "49000",
    })

    assert not form.is_valid()
    assert "email" in form.errors


@pytest.mark.django_db
def test_order_form_email_valid():
    form = OrderCreateForm(data={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "address": "Main Street 1",
        "city": "Dnipro",
        "postal_code": "49000",
    })

    assert form.is_valid()
    assert form.cleaned_data["email"] == "john@example.com"


@pytest.mark.django_db
def test_register_form_valid():
    form = RegisterForm(data={
        "username": "testuser",
        "email": "test@example.com",
        "password1": "StrongPassword123!",
        "password2": "StrongPassword123!",
    })

    assert form.is_valid()


@pytest.mark.django_db
def test_register_form_password_mismatch():
    form = RegisterForm(data={
        "username": "testuser",
        "email": "test@example.com",
        "password1": "StrongPassword123!",
        "password2": "DifferentPassword123!",
    })

    assert not form.is_valid()
    assert "password2" in form.errors


@pytest.mark.django_db
def test_register_form_username_required():
    form = RegisterForm(data={
        "username": "",
        "email": "test@example.com",
        "password1": "StrongPassword123!",
        "password2": "StrongPassword123!",
    })

    assert not form.is_valid()
    assert "username" in form.errors


@pytest.mark.django_db
def test_register_form_email():
    form = RegisterForm(data={
        "username": "testuser",
        "email": "test@example.com",
        "password1": "StrongPassword123!",
        "password2": "StrongPassword123!",
    })

    assert form.is_valid()
    assert form.cleaned_data["email"] == "test@example.com"
