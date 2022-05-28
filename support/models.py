from datetime import datetime
from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    subject = models.CharField(max_length=250)
    message = models.TextField()
    contact_date = models.DateField(auto_now_add=True)

class FAQ(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()
