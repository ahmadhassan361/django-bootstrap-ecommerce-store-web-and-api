from django.db import models
from customers import models as cmodels
from app import models as gmodels
from django.utils.safestring import mark_safe

# Create your models here.
ORDER_STATUS = (
    ('pending', 'PENDING'),
    ('processing', 'PROCESSING'),
    ('shipped', 'SHIPPED'),
    ('delivered', 'DELIVERED'),
    ('cancelled', 'CANCELLED'),
    ('rejected', 'REJECTED')
)
class ShippingCharges(models.Model):
    charges = models.IntegerField()

class Order(models.Model):
    order_id = models.CharField(max_length=250,unique=True,blank=True)
    customer = models.ForeignKey(cmodels.Customer, on_delete=models.CASCADE)
    status = models.CharField(
        default="pending", max_length=50, choices=ORDER_STATUS)
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(default=0)
    shipping_fee = models.IntegerField(default=0)
    check_out = models.BooleanField(default=False)
    cancel_reason = models.TextField(blank=True)

    def update_model(self):
        Order.objects.filter(pk=self.id).update(order_id = str(13990894890+self.id))
        


    def save(self, *args, **kwargs):
            super(Order, self).save(*args, **kwargs)
            self.update_model() # Call the funct
   

    def __str__(self) -> str:
        return self.customer.fullname + " " + str(self.date)

class OrderItem(models.Model):
    product = models.ForeignKey(gmodels.Stock, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def image_preview(self):
        if self.product.product.image:
            return mark_safe('<img src="{}" width="120" height="120" style="border-radius: 10px;" />'.format(self.product.product.image.url))
        return ""
    @property
    def image_preview_inside(self):
        if self.product.product.image:
            return mark_safe('<img src="{}" width="120" height="120" style="border-radius: 5px;"/>'.format(self.product.product.image.url))
        return ""
    

    def __str__(self):
        return self.product.product.title +" ("+ str(self.product.product.category) +")"



    
