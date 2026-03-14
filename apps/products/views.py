from rest_framework import viewsets
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        lang = request.GET.get("lang", "ru")
        queryset = self.get_queryset()
        data = []

        for product in queryset:
            if lang == "uz":
                name = product.product_name_uz
            elif lang == "kz":
                name = product.product_name_kz
            else:
                name = product.product_name_ru
            price = product.new_price if product.new_price else product.old_price
            data.append({
                "id": product.id,
                "name": name,
                "image": product.image.url if product.image else None,
                "old_price": product.old_price,
                "new_price": product.new_price,
                "price": price
            })

        return Response(data)