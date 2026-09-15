from django.db import models
from books.models import Book
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    first_name = models.CharField(
        max_length=100,
        verbose_name=_("First name"),
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name=_("Last name"),
    )

    email = models.EmailField(
        verbose_name=_("Email"),
    )

    address = models.CharField(
        max_length=250,
        verbose_name=_("Address"),
    )

    city = models.CharField(
        max_length=100,
        verbose_name=_("City"),
    )

    postal_code = models.CharField(
        max_length=20,
        verbose_name=_("Postal code"),
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created"),
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated"),
    )

    paid = models.BooleanField(
        default=False,
        verbose_name=_("Paid"),
    )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"Order: {self.id} - {self.first_name} {self.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Order"),
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name=_("Book"),
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Price"),
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantity"),
    )

    class Meta:
        verbose_name = _("Order item")
        verbose_name_plural = _("Order items")

    def __str__(self):
        return f"{self.order} - {self.book} {self.quantity}шт. {self.price}грн"

    def get_cost(self):
        return self.price * self.quantity