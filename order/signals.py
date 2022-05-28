from django.db.models.signals import post_save
from django.dispatch import receiver

import customers
from .models import Order,OrderItem
from django.core.mail import EmailMessage  
from django.template.loader import render_to_string  
from django.contrib.sites.shortcuts import get_current_site 

 
# @receiver(post_save, sender=Order)
# def order_created(sender, instance, created, **kwargs):
#     if not created:
#         print("order updated")
        
#         if instance.check_out:
#             print(instance.status)
#             send_email(instance=instance)
#     else:
#         print("order created")


