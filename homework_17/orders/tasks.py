from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Sum
from .models import Order
from django.core.management import call_command


@shared_task
def send_order_email(order_id, email):
    send_mail(
        subject="Ваше замовлення створено",
        message=(
            f"Дякуємо за замовлення! "
            f"Номер вашого замовлення: {order_id}."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


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

@shared_task
def clear_expired_sessions():
    call_command("clearsessions")
    print("Expired sessions cleared")