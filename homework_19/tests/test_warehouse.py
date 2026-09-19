from unittest.mock import patch

import pytest
from rest_framework.test import APIClient

from books.models import Book, Category
from books.services.warehouse import (
    InventoryNotFoundError,
    WarehouseServiceError,
    get_inventory,
)
from users.models import User


@pytest.mark.django_db
def test_get_inventory_success():
    mock_response = {
        "id": 1,
        "product_id": 1,
        "quantity": 10,
        "updated_at": "2026-09-18T06:05:31.462861Z",
    }

    with patch("books.services.warehouse.requests.get") as mock_get:
        mock_get.return_value.json.return_value = [mock_response]
        mock_get.return_value.raise_for_status.return_value = None

        result = get_inventory(1)

    assert result == mock_response
    mock_get.assert_called_once()


@pytest.mark.django_db
def test_get_inventory_not_found():
    with patch("books.services.warehouse.requests.get") as mock_get:
        mock_get.return_value.json.return_value = []
        mock_get.return_value.raise_for_status.return_value = None

        with pytest.raises(InventoryNotFoundError):
            get_inventory(999999)


@pytest.mark.django_db
def test_get_inventory_service_error():
    import requests

    with patch(
        "books.services.warehouse.requests.get",
        side_effect=requests.RequestException("Connection error"),
    ):
        with pytest.raises(WarehouseServiceError):
            get_inventory(1)


@pytest.mark.django_db
def test_inventory_endpoint_success():
    category = Category.objects.create(
        name="Test Category",
        slug="test-category",
    )

    book = Book.objects.create(
        title="Test Book",
        author="Test Author",
        price=100,
        description="Test",
        stock=10,
        category=category,
    )

    user = User.objects.create_superuser(
        username="warehouse_test_admin",
        email="warehouse_test@example.com",
        password="StrongTestPassword123!",
    )

    client = APIClient()
    client.force_authenticate(user=user)

    inventory = {
        "id": 1,
        "product_id": book.id,
        "quantity": 15,
        "updated_at": "2026-09-18T06:05:31.462861Z",
    }

    with patch(
        "books.views.get_inventory",
        return_value=inventory,
    ):
        response = client.get(
            f"/api/books/{book.id}/inventory/",
            HTTP_HOST="localhost",
        )

    assert response.status_code == 200
    assert response.data["book_id"] == book.id
    assert response.data["quantity"] == 15


@pytest.mark.django_db
def test_inventory_endpoint_not_found():
    category = Category.objects.create(
        name="Test Category",
        slug="test-category",
    )

    book = Book.objects.create(
        title="Test Book",
        author="Test Author",
        price=100,
        description="Test",
        stock=10,
        category=category,
    )

    user = User.objects.create_superuser(
        username="warehouse_test_admin_404",
        email="warehouse_test_404@example.com",
        password="StrongTestPassword123!",
    )

    client = APIClient()
    client.force_authenticate(user=user)

    with patch(
        "books.views.get_inventory",
        side_effect=InventoryNotFoundError(book.id),
    ):
        response = client.get(
            f"/api/books/{book.id}/inventory/",
            HTTP_HOST="localhost",
        )

    assert response.status_code == 404
    assert response.data["detail"] == "Inventory not found."


@pytest.mark.django_db
def test_inventory_endpoint_service_unavailable():
    category = Category.objects.create(
        name="Test Category",
        slug="test-category",
    )

    book = Book.objects.create(
        title="Test Book",
        author="Test Author",
        price=100,
        description="Test",
        stock=10,
        category=category,
    )

    user = User.objects.create_superuser(
        username="warehouse_test_admin_503",
        email="warehouse_test_503@example.com",
        password="StrongTestPassword123!",
    )

    client = APIClient()
    client.force_authenticate(user=user)

    with patch(
        "books.views.get_inventory",
        side_effect=WarehouseServiceError(),
    ):
        response = client.get(
            f"/api/books/{book.id}/inventory/",
            HTTP_HOST="localhost",
        )

    assert response.status_code == 503
    assert response.data["detail"] == "Warehouse service unavailable."
