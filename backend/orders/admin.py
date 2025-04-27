from django.contrib import admin

from orders.models import Order, OrderItem, Product


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ("id", "api_id", "product", "quantity", "order", "get_total_price")
    autocomplete_fields = ("product",)
    readonly_fields = ("order", "api_id", "get_total_price")
    show_change_link = True
    list_select_related = ("product",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    fields = ("id", "api_id", "added_at", "updated_at", "order", "product", "quantity")
    readonly_fields = ("id", "api_id", "added_at", "updated_at", "get_total_price")
    autocomplete_fields = ("order", "product")
    list_display = (
        "id",
        "api_id",
        "added_at",
        "order",
        "product",
        "quantity",
        "get_total_price",
    )
    search_fields = ("api_id",)
    list_filter = ("added_at", "updated_at")
    list_select_related = ("order", "product")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ("id", "api_id", "added_at", "updated_at", "name", "description", "price")
    readonly_fields = ("id", "api_id", "added_at", "updated_at")
    search_fields = ("id", "api_id", "name")
    list_filter = ("added_at", "updated_at")
    list_display = ("api_id", "added_at", "name", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = (
        "id",
        "api_id",
        "added_at",
        "updated_at",
        "customer",
        "supplier",
        "status",
        "get_total_price",
    )
    readonly_fields = ("id", "api_id", "added_at", "updated_at", "get_total_price")
    autocomplete_fields = ("customer", "supplier")
    list_display = (
        "id",
        "api_id",
        "added_at",
        "customer",
        "supplier",
        "status",
        "get_total_price",
    )
    search_fields = (
        "api_id",
        "customer__name",
        "customer__api_id",
        "supplier__name",
        "supplier__api_id",
    )
    list_filter = ("status", "added_at", "updated_at")
    inlines = [OrderItemInline]

    def get_queryset(self, request):
        """
        Override the get_queryset method to include the related fields in the queryset.
        """
        return (
            super()
            .get_queryset(request)
            .select_related("customer", "supplier")
            .prefetch_related("items", "items__product")
        )
