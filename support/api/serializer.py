from rest_framework import serializers
from .. import models
class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FAQ
        fields = '__all__'