from django.urls import path

from .views import InventoryDetailView, InventoryListCreateView

urlpatterns = [
    path("", InventoryListCreateView.as_view(), name="inventory-list"),
    path("<int:pk>/", InventoryDetailView.as_view(), name="inventory-detail"),
]
