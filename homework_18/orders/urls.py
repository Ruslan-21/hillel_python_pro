from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path(
        "create/",
        views.order_create,
        name="order_create",
    ),

    path(
        "<int:order_id>/create-checkout-session/",
        views.create_checkout_session,
        name="create_checkout_session",
    ),

    path(
        "payment/success/",
        views.payment_success,
        name="payment_success",
    ),

    path(
        "payment/cancel/",
        views.payment_cancel,
        name="payment_cancel",
    ),
]