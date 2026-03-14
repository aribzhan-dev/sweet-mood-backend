from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction

from .models import Order, OrderItem
from .serializers import OrderCreateSerializer
from apps.products.models import Product

from services.telegram_service import send_order_to_telegram


class OrderViewSet(viewsets.GenericViewSet):
    serializer_class = OrderCreateSerializer
    http_method_names = ["post"]

    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        items_data = serializer.validated_data.pop("items")
        order = Order.objects.create(
            total_price=0,
            **serializer.validated_data
        )
        total_price = 0
        created_items = []

        for item in items_data:
            product_id = item["product_id"]
            quantity = item["quantity"]
            product = Product.objects.get(id=product_id)
            price = product.actual_price()
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )

            created_items.append(order_item)
            total_price += price * quantity

        order.total_price = total_price
        order.save()

        send_order_to_telegram(order)
        return Response(
            {
                "message": "Order created successfully",
                "order_id": order.id,
                "total_price": total_price
            },
            status=status.HTTP_201_CREATED
        )