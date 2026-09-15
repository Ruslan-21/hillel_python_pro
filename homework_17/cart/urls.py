from django.urls import path
from . import views
from .views import CreateCheckoutSessionView

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<int:book_id>/", views.cart_add, name="cart_add"),
    path("remove/<int:book_id>/", views.cart_remove, name="cart_remove"),
    path("create-checkout-session/", CreateCheckoutSessionView.as_view(), name="create_checkout_session"),
]