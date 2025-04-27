from rest_framework import serializers

from accounts.models import Company, Contact
from orders.models import Order, OrderItem, Product


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "api_id",
            "phone_number",
            "postal_code",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "country",
        ]
        read_only_fields = ["api_id"]


class CompanySerializer(serializers.ModelSerializer):
    contact = serializers.SlugRelatedField(
        slug_field="api_id",
        queryset=Contact.objects.all(),
        allow_null=True,
        required=False,
        help_text="Contact information for the company",
    )

    class Meta:
        model = Company
        fields = ["api_id", "name", "added_at", "contact"]
        read_only_fields = ["api_id", "added_at", "contact"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["api_id", "name", "description", "price"]
        read_only_fields = ["api_id"]


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(
        slug_field="api_id",
        queryset=Company.objects.all(),
        help_text="Customer company for the order",
    )
    supplier = serializers.SlugRelatedField(
        slug_field="api_id",
        queryset=Company.objects.all(),
        help_text="Supplier company for the order",
    )
    total_price = serializers.ReadOnlyField(help_text="Total price of the order")
    items_count = serializers.ReadOnlyField(help_text="Number of items in the order")

    class Meta:
        model = Order
        fields = [
            "api_id",
            "added_at",
            "updated_at",
            "customer",
            "supplier",
            "status",
            "total_price",
            "items_count",
        ]
        read_only_fields = ["api_id"]


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.SlugRelatedField(
        slug_field="api_id",
        queryset=Order.objects.all(),
        help_text="Order to which this item belongs",
    )
    product = serializers.SlugRelatedField(
        slug_field="api_id",
        queryset=Product.objects.all(),
        help_text="Product in the order item",
    )

    class Meta:
        model = OrderItem
        fields = ["api_id", "order", "product", "quantity"]
        read_only_fields = ["api_id"]
