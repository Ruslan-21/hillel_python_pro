"""
URL configuration for bookstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from books.api_urls import urlpatterns as books_api_urls
from orders.api_urls import urlpatterns as orders_api_urls
from cart.api_urls import urlpatterns as cart_api_urls


def home_page(request):
    return redirect("books:list")


urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/", include(books_api_urls)),
    path("api/", include(orders_api_urls)),
    path("api/", include(cart_api_urls)),

    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/token/verify/",
        TokenVerifyView.as_view(),
        name="token_verify",
    ),
]

urlpatterns += i18n_patterns(
    path("", home_page),
    path("books/", include("books.urls")),
    path("users/", include("users.urls")),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
)

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]