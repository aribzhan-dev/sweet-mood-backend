from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product_name_ru",
        "product_name_kz",
        "product_name_uz",
        "old_price",
        "new_price",
        "created_at",
    )

    search_fields = (
        "product_name_ru",
        "product_name_kz",
        "product_name_uz",
    )

    list_filter = ("created_at",)

    ordering = ("-created_at",)