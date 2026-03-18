from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer_name",
        "whatsapp_phone",
        "order_type",
        "total_price",
        "payment_check_link",
        "status",
        "created_at",
    )

    list_filter = ("status", "order_type", "created_at")

    search_fields = ("name", "surname", "phone_number")

    # statusni list sahifasidan o'zgartirish
    list_editable = ("status",)

    readonly_fields = (
        "total_price",
        "payment_check_preview",
        "created_at",
    )

    inlines = [OrderItemInline]

    ordering = ("-created_at",)

    fieldsets = (
        ("Customer info", {
            "fields": ("name", "surname", "phone_number")
        }),
        ("Order info", {
            "fields": ("order_type", "status", "total_price")
        }),
        ("Payment", {
            "fields": ("payment_check_preview",)
        }),
        ("System", {
            "fields": ("created_at",)
        }),
    )

    def customer_name(self, obj):
        return f"{obj.name} {obj.surname}"
    customer_name.short_description = "Customer"

    def whatsapp_phone(self, obj):
        phone = obj.phone_number.replace("+", "")
        return format_html(
            '<a href="https://wa.me/{}" target="_blank">{}</a>',
            phone,
            obj.phone_number
        )
    whatsapp_phone.short_description = "Phone"

    def payment_check_link(self, obj):
        if obj.payment_check_file:
            return format_html(
                '<a href="{}" target="_blank">Open file</a>',
                obj.payment_check_file.url
            )
        return "-"
    payment_check_link.short_description = "Payment check"

    def payment_check_preview(self, obj):
        if obj.payment_check_file:
            return format_html(
                '<a href="{}" target="_blank">Open payment check</a>',
                obj.payment_check_file.url
            )
        return "No file"
    payment_check_preview.short_description = "Payment check"