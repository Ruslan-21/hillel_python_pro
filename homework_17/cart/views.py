from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

# Create your views here.


from books.models import Book
from .cart import Cart
from .forms import CartAddBookForm
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View


@require_POST
def cart_add(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    form = CartAddBookForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            book=book,
            quantity=cd["quantity"],
            update_quantity=cd["override"]
        )

    return redirect("cart:cart_detail")



def cart_remove(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(
        request,
        "cart/detail.html",
        {
            "cart": cart,
        },
    )



stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def post(self, request):
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Books",
                        },
                        "unit_amount": 1000,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="http://localhost:8000/success/",
            cancel_url="http://localhost:8000/cancel/",
        )

        return JsonResponse({
            "id": session.id
        })


stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def post(self, request):
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Books",
                        },
                        "unit_amount": 1000,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="http://localhost:8000/success/",
            cancel_url="http://localhost:8000/cancel/",
        )

        return JsonResponse({
            "id": session.id
        })