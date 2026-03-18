import json
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Order, OrderItem
from .serializers import OrderCreateSerializer
from apps.products.models import Product

from services.telegram_service import send_order_to_telegram


class OrderViewSet(viewsets.GenericViewSet):
    serializer_class = OrderCreateSerializer
    http_method_names = ["post"]

    parser_classes = (MultiPartParser, FormParser)

    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        items_data = request.data.get("items")

        try:
            items_data = json.loads(items_data)
        except Exception:
            return Response(
                {"error": "Items must be valid JSON"},
                status=status.HTTP_400_BAD_REQUEST
            )
        order = Order.objects.create(
            name=serializer.validated_data["name"],
            surname=serializer.validated_data["surname"],
            phone_number=serializer.validated_data["phone_number"],
            order_type=serializer.validated_data["order_type"],
            location=serializer.validated_data["location"],
            payment_check_file=serializer.validated_data["payment_check_file"],
            total_price=0
        )

        total_price = 0

        for item in items_data:

            product = get_object_or_404(Product, id=item["product_id"])

            quantity = int(item["quantity"])

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

        return Response(
            {
                "message": "Order created successfully",
                "order_id": order.id,
                "total_price": total_price
            },
            status=status.HTTP_201_CREATED
        )