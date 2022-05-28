from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    fullname = models.CharField(max_length=250,blank=True)
    mobile_no = models.CharField(max_length=15,blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=250,blank=True)
    zipcode = models.CharField(max_length=20,blank=True)
    province = models.CharField(max_length=250,blank=True)
    

    def __str__(self) -> str:
        return self.user.username

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)