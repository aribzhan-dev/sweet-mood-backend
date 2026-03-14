from django.db import models

class Product(models.Model):
    product_name_ru = models.CharField(max_length=255)
    product_name_kz = models.CharField(max_length=255)
    product_name_uz = models.CharField(max_length=255)
    image = models.ImageField(upload_to="products/")
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    new_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def actual_price(self):
        if self.new_price:
            return self.new_price
        return self.old_price

    def __str__(self):
        return self.product_name_kz