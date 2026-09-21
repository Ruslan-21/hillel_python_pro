from rest_framework import generics

from .models import Inventory
from .serializers import InventorySerializer


class InventoryListCreateView(generics.ListCreateAPIView):
    serializer_class = InventorySerializer

    def get_queryset(self):
        queryset = Inventory.objects.all()

        product_id = self.request.query_params.get("product_id")

        if product_id:
            queryset = queryset.filter(product_id=product_id)

        return queryset


class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
