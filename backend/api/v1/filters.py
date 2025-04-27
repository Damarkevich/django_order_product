from django_filters import rest_framework as filters

from orders.models import Product


class ProductFilter(filters.FilterSet):
    """
    FilterSet for Product model.
    """

    customer = filters.CharFilter(field_name="customer__api_id", lookup_expr="exact")
    supplier = filters.CharFilter(field_name="supplier__api_id", lookup_expr="exact")

    class Meta:
        model = Product
        fields = {
            "price": ["exact", "lt", "gt"],
            "supplier": ["exact"],
            "customer": ["exact"],
        }
