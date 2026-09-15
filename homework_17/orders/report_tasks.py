from celery import shared_task
from django.db.models import Sum
from .models import Order


@shared_task
def generate_orders_report():
    total_orders = Order.objects.count()
    total_items = Order.objects.aggregate(
        total=Sum("items__quantity")
    )["total"] or 0

    report = {
        "total_orders": total_orders,
        "total_items": total_items,
    }

    print(f"Orders report: {report}")

    return report