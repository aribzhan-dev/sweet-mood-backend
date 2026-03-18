import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.db import transaction

from .models import Order, OrderItem
from .serializers import OrderCreateSerializer
from apps.products.models import Product

from services.telegram_service import send_order_to_telegram


class OrderViewSet(viewsets.GenericViewSet):
    serializer_class = OrderCreateSerializer
    http_method_names = ["post"]

    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @transaction.atomic
    def create(self, request):
        data = request.data.copy()

        if "items" in data and isinstance(data["items"], str):
            data["items"] = json.loads(data["items"])

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        items_data = serializer.validated_data.pop("items")

        order = Order.objects.create(
            total_price=0,
            **serializer.validated_data
        )

        total_price = 0

        for item in items_data:
            product = Product.objects.get(id=item["product_id"])
            quantity = item["quantity"]
            price = product.actual_price()
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )
            total_price += price * quantity

        order.total_price = total_price
        order.save()

        send_order_to_telegram(order)

        return Response({
            "message": "Order created",
            "order_id": order.id
        })