from dataclasses import field
from itertools import product
from pydoc import classname
from pyexpat import model
from unicodedata import category
from django.db.models import fields
from rest_framework import serializers
from .. import models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id','title','image','short_desc']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubCategory
        fields = ['id','title','image','category']

class SubSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubSubCategory
        fields = ['id','title','category']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    class Meta:
        model = models.Product
        fields = '__all__'

class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductColor
        fields = '__all__'
class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductSize
        fields = '__all__'
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = '__all__'
class StockSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = models.Stock
        fields = '__all__'
class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Slider
        fields = '__all__'

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Offer
        fields = '__all__'
class HeaderBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HeaderBanner 
        fields = '__all__'