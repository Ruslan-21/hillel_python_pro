from django.db import transaction
from .models import Order, OrderItem
from .forms import OrderCreateForm
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from cart.cart import Cart
import stripe
from django.urls import reverse


stripe.api_key = settings.STRIPE_SECRET_KEY


@transaction.atomic
def order_create(request):
    cart = Cart(request)

    if request.method == "POST":
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    book=item["book"],
                    price=item["price"],
                    quantity=item["quantity"],
                )

            send_mail(
                subject="Ваше замовлення створено",
                message=(
                    f"Дякуємо за замовлення! "
                    f"Номер вашого замовлення: {order.id}."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.email],
                fail_silently=False,
            )

            return render(
                request,
                "orders/order_created.html",
                {"order": order},
            )

    else:
        form = OrderCreateForm()

    return render(
        request,
        "orders/order_create.html",
        {
            "cart": cart,
            "form": form,
        },
    )


def create_checkout_session(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    line_items = []

    for item in order.items.all():
        line_items.append(
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": item.book.title,
                    },
                    "unit_amount": int(item.price * 100),
                },
                "quantity": item.quantity,
            }
        )

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("orders:payment_success")
        ),
        cancel_url=request.build_absolute_uri(
            reverse("orders:payment_cancel")
        ),
    )

    return redirect(session.url)


def payment_success(request):
    return render(
        request,
        "orders/payment_success.html",
    )


def payment_cancel(request):
    return render(
        request,
        "orders/payment_cancel.html",
    )