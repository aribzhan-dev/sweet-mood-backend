import json
import logging

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.db import transaction

from .models import Order, OrderItem
from .serializers import OrderCreateSerializer
from apps.products.models import Product
from services.telegram_service import send_order_to_telegram

logger = logging.getLogger(__name__)


class OrderViewSet(viewsets.GenericViewSet):
    serializer_class = OrderCreateSerializer
    http_method_names = ["post"]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request):
        data = {}
        for key in request.data:
            data[key] = request.data[key]

        items_raw = data.get("items")
        if items_raw and isinstance(items_raw, str):
            try:
                data["items"] = json.loads(items_raw)
            except json.JSONDecodeError:
                logger.error(f"items JSON parse xatoligi: {items_raw}")
                return Response(
                    {"error": "items maydoni noto'g'ri JSON formatda"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # payment_check_file ni alohida olamiz (QueryDict dan tushib qolmasligi uchun)
        if "payment_check_file" in request.FILES:
            data["payment_check_file"] = request.FILES["payment_check_file"]

        logger.info(f"Kelgan data keys: {list(data.keys())}")
        logger.info(f"items: {data.get('items')}")

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            logger.error(f"Serializer xatolari: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = self._create_order(serializer.validated_data)
        except Product.DoesNotExist as e:
            logger.error(f"Mahsulot topilmadi: {e}")
            return Response(
                {"error": "Mahsulot topilmadi"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(f"Order yaratishda xatolik: {e}")
            return Response(
                {"error": "Server xatoligi, qaytadan urinib ko'ring"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Telegram transaksiyadan TASHQARIDA — xato bo'lsa order saqlanib qoladi
        try:
            send_order_to_telegram(order)
        except Exception as e:
            logger.error(f"Telegram xatoligi (order #{order.id}): {e}")

        return Response(
            {"message": "Order yaratildi", "order_id": order.id},
            status=status.HTTP_201_CREATED
        )

    @transaction.atomic
    def _create_order(self, validated_data):
        items_data = validated_data.pop("items")

        order = Order.objects.create(total_price=0, **validated_data)

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
        return order