from django.contrib import admin
from django.utils.html import format_html
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "image_preview",
        "product_name_ru",
        "product_name_uz",
        "product_name_kz",
        "price_display",
        "created_at",
    )

    search_fields = (
        "product_name_ru",
        "product_name_uz",
        "product_name_kz",
    )

    readonly_fields = ("image_preview", "created_at")

    list_filter = ("created_at",)

    ordering = ("-created_at",)

    fieldsets = (
        ("Product names", {
            "fields": (
                "product_name_ru",
                "product_name_uz",
                "product_name_kz",
            )
        }),

        ("Image", {
            "fields": (
                "image",
                "image_preview",
            )
        }),

        ("Pricing", {
            "fields": (
                "old_price",
                "new_price",
            )
        }),

        ("System", {
            "fields": (
                "created_at",
            )
        }),
    )


    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:80px;height:80px;object-fit:cover;border-radius:8px;" />',
                obj.image.url
            )
        return "No image"

    image_preview.short_description = "Image"


    def price_display(self, obj):

        if obj.new_price:
            return format_html(
                '<span style="text-decoration:line-through;color:#888;">{} ₸</span> '
                '<b style="color:#e53935;">{} ₸</b>',
                obj.old_price,
                obj.new_price
            )

        return format_html("<b>{} ₸</b>", obj.old_price)

    price_display.short_description = "Price"