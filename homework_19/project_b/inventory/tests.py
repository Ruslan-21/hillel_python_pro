from django.core.cache import cache
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User

from .models import Inventory
from .tasks import get_inventory_summary


@override_settings(ALLOWED_HOSTS=["testserver"])
class InventoryAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword123",
        )

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.inventory = Inventory.objects.create(
            product_id=100,
            quantity=10,
        )

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def tearDown(self):
        cache.clear()

    def test_inventory_list(self):
        self.authenticate()

        response = self.client.get(
            "/api/inventory/",
            HTTP_HOST="testserver",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["product_id"], 100)

    def test_inventory_create(self):
        self.authenticate()

        response = self.client.post(
            "/api/inventory/",
            {
                "product_id": 200,
                "quantity": 25,
            },
            format="json",
            HTTP_HOST="testserver",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(Inventory.objects.filter(product_id=200).exists())

    def test_inventory_detail(self):
        self.authenticate()

        response = self.client.get(
            f"/api/inventory/{self.inventory.id}/",
            HTTP_HOST="testserver",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["quantity"],
            10,
        )

    def test_inventory_update(self):
        self.authenticate()

        response = self.client.patch(
            f"/api/inventory/{self.inventory.id}/",
            {"quantity": 50},
            format="json",
            HTTP_HOST="testserver",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.inventory.refresh_from_db()

        self.assertEqual(
            self.inventory.quantity,
            50,
        )

    def test_inventory_delete(self):
        self.authenticate()

        response = self.client.delete(
            f"/api/inventory/{self.inventory.id}/",
            HTTP_HOST="testserver",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(Inventory.objects.filter(id=self.inventory.id).exists())

    def test_inventory_not_found(self):
        self.authenticate()

        response = self.client.get(
            "/api/inventory/99999/",
            HTTP_HOST="testserver",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )


class InventoryTaskTestCase(TestCase):
    def tearDown(self):
        cache.clear()

    def test_inventory_summary(self):
        Inventory.objects.create(
            product_id=1,
            quantity=10,
        )
        Inventory.objects.create(
            product_id=2,
            quantity=20,
        )

        result = get_inventory_summary()

        self.assertEqual(
            result,
            {
                "total_products": 2,
                "total_quantity": 30,
            },
        )

    def test_inventory_summary_uses_cache(self):
        Inventory.objects.create(
            product_id=1,
            quantity=10,
        )

        first_result = get_inventory_summary()
        second_result = get_inventory_summary()

        self.assertEqual(
            first_result,
            second_result,
        )
        self.assertEqual(
            second_result["total_products"],
            1,
        )
        self.assertEqual(
            second_result["total_quantity"],
            10,
        )

    def test_inventory_summary_cache_invalidation(self):
        Inventory.objects.create(
            product_id=1,
            quantity=10,
        )

        get_inventory_summary()

        self.assertIsNotNone(cache.get("inventory_summary"))

        Inventory.objects.create(
            product_id=2,
            quantity=20,
        )

        self.assertIsNone(cache.get("inventory_summary"))
