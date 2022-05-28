from rest_framework import serializers
from .. import models
from app.api.serializer import StockSerializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product = StockSerializer()
    class Meta:
        model = models.OrderItem
        fields = '__all__'
class ShippingChargesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShippingCharges
        fields = '__all__'
