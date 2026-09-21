from celery import shared_task
from django.core.cache import cache

from .models import Inventory


@shared_task
def get_inventory_summary():
    cache_key = "inventory_summary"

    cached_result = cache.get(cache_key)

    if cached_result is not None:
        return cached_result

    total_products = Inventory.objects.count()
    total_quantity = sum(Inventory.objects.values_list("quantity", flat=True))

    result = {
        "total_products": total_products,
        "total_quantity": total_quantity,
    }

    cache.set(cache_key, result, 60)

    return result
