from accounts.models import Company, Contact
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from orders.models import Order, OrderItem, Product
from rest_framework import filters, pagination, permissions, viewsets

from api.v1.serializers import (
    CompanySerializer,
    ContactSerializer,
    OrderItemSerializer,
    OrderSerializer,
    ProductSerializer,
)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "phone_number",
        "postal_code",
        "city",
        "state",
        "country",
        "address_line_1",
        "address_line_2",
    ]
    ordering_fields = ["city", "state", "country"]
    lookup_field = "api_id"


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["name"]
    search_fields = ["name"]
    lookup_field = "api_id"


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["price", "added_at"]
    search_fields = ["name"]
    lookup_field = "api_id"


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["customer__api_id", "supplier__api_id", "status"]
    ordering_fields = ["added_at"]
    search_fields = ["customer__name", "supplier__name"]
    lookup_field = "api_id"

    def get_queryset(self):
        return Order.objects.select_related("customer", "supplier").annotate(
            items_count=models.Count("items"),
            # Calculate the total price of the order by summing the price of each product in the order items
            total_price=models.Sum(
                models.F("items__product__price") * models.F("items__quantity")
            ),
        )


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = ["order__api_id", "product__api_id"]
    ordering_fields = ["added_at"]
    lookup_field = "api_id"
