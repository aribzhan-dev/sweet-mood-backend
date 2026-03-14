from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.models import Product


class OrderItemCreateSerializer(serializers.Serializer):

    product_id = serializers.IntegerField()

    quantity = serializers.IntegerField()


class OrderCreateSerializer(serializers.ModelSerializer):

    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "name",
            "surname",
            "phone_number",
            "location",
            "order_type",
            "payment_check_file",
            "items",
        )