from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import stripe

from cart.cart import Cart

from .forms import OrderCreateForm
from .models import Order, OrderItem
from .serializers import OrderSerializer


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


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related(
        "items__book"
    ).all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in [
            "update",
            "partial_update",
            "destroy",
        ]:
            return [IsAdminUser()]

        return [IsAuthenticated()]

    @transaction.atomic
    def perform_create(self, serializer):
        cart = Cart(self.request)

        order = serializer.save()

        for item in cart:
            OrderItem.objects.create(
                order=order,
                book=item["book"],
                price=item["price"],
                quantity=item["quantity"],
            )

        cart.clear()