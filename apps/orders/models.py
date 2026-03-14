from django.db import models
from apps.products.models import Product


class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ("delivery", "Delivery"),
        ("pickup", "Self pickup"),
    ]
    STATUS_CHOICES = [
        ("order_received", "Order Received"),
        ("in_progress", "In Progress"),
        ("delivered", "Delivered"),
    ]
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=30)
    location = models.CharField(max_length=255)
    order_type = models.CharField(
        max_length=20,
        choices=ORDER_TYPE_CHOICES
    )
    payment_check_file = models.FileField(
        upload_to="payment_checks/",
        null=True,
        blank=True
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="order_received",
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product} x {self.quantity}"