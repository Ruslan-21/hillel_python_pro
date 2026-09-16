import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from users.forms import RegisterForm


User = get_user_model()


@pytest.mark.django_db
def test_register_form_valid():
    form = RegisterForm(
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_register_form_password_mismatch():
    form = RegisterForm(
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password1": "StrongPassword123!",
            "password2": "DifferentPassword123!",
        }
    )

    assert not form.is_valid()


@pytest.mark.django_db
def test_register_form_username_required():
    form = RegisterForm(
        data={
            "username": "",
            "email": "test@example.com",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        }
    )

    assert not form.is_valid()
    assert "username" in form.errors


@pytest.mark.django_db
def test_register_view_get(client):
    response = client.get(reverse("register"))

    assert response.status_code == 200
    assert isinstance(response.context["form"], RegisterForm)


@pytest.mark.django_db
def test_register_view_creates_user(client):
    response = client.post(
        reverse("register"),
        data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        },
    )

    assert response.status_code == 302
    assert User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_register_view_redirects_to_login(client):
    response = client.post(
        reverse("register"),
        data={
            "username": "redirectuser",
            "email": "redirect@example.com",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("login")
