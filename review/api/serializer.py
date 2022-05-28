from rest_framework import serializers

from customers.api.serializer import CustomerSerializer
from .. import models 

class ProductReviewSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = models.ProductReview
        fields = '__all__'