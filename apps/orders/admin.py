from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "surname",
        "phone_number",
        "order_type",
        "status",
        "total_price",
        "created_at",
    )

    list_filter = ("status", "order_type")

    search_fields = ("phone_number", "name")

    inlines = [OrderItemInline]

    ordering = ("-created_at",)