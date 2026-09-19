from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Inventory


@receiver(post_save, sender=Inventory)
@receiver(post_delete, sender=Inventory)
def invalidate_inventory_cache(sender, instance, **kwargs):
    cache.delete("inventory_summary")
