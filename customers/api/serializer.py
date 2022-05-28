import imp
from rest_framework import serializers
from django.contrib.auth.models import User
from .. import models
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id','username','email','is_active']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','email','is_active')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.is_active = False
        user.set_password(validated_data['password'])
        user.save()


        return user

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.Customer
        fields = '__all__'