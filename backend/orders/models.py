from django.db import models
from core.models import BaseModel
from django.contrib import admin


class Product(BaseModel):
    name = models.CharField(max_length=255)
    price = models.IntegerField(help_text="Price in cents")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.name} - {self.price}"


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"
    CANCELLED = "cancelled", "Cancelled"


class Order(BaseModel):
    customer = models.ForeignKey(
        "accounts.Company",
        on_delete=models.PROTECT,
        related_name="customer_orders",
        help_text="Customer who placed the order",
    )
    supplier = models.ForeignKey(
        "accounts.Company",
        on_delete=models.PROTECT,
        related_name="supplier_orders",
        help_text="Supplier who will fulfill the order",
    )
    products = models.ManyToManyField(
        Product,
        through="OrderItem",
        related_name="orders",
        help_text="Products in the order",
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        help_text="Current status of the order",
    )

    def __str__(self):
        return f"{self.id} - {self.added_at.strftime('%Y-%m-%d')}"

    @admin.display(description="Total Price")
    def total_price(self) -> int:
        return sum(item.total_price() for item in self.items.all())


class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        help_text="Order to which this item belongs",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items",
        help_text="Product in the order",
    )
    quantity = models.PositiveIntegerField(help_text="Quantity of the product")

    def __str__(self):
        return f"{self.id} - {self.product.name} (x{self.quantity})"

    @admin.display(description="Total Price")
    def total_price(self) -> int:
        return self.product.price * self.quantity
