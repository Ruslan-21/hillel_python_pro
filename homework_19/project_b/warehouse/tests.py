from django.test import TestCase
from django.urls import reverse


class InternationalizationTestCase(TestCase):
    def test_set_language_to_ukrainian(self):
        response = self.client.post(
            reverse("set_language"),
            {
                "language": "uk",
                "next": "/",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.cookies["django_language"].value,
            "uk",
        )
