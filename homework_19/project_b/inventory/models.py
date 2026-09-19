from django.db import models

# Create your models here.


class Inventory(models.Model):
    product_id = models.PositiveIntegerField(unique=True)
    quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Product {self.product_id}: {self.quantity}"
