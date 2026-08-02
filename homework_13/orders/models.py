from django.db import models
from django.db.models import CASCADE
from books.models import Book


# Create your models here.


class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order: {self.id} - {self.first_name} {self.last_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
      )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,

    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    quantity = models.PositiveIntegerField(
        default=1
    )
    def __str__(self):
        return f"{self.order} - {self.book}  {self.quantity}шт. {self.price}грн"


    def get_cost(self):
        return self.price * self.quantity