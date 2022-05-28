from django.db import models
from customers import models as cmodels
from app import models as gmodels
# Create your models here.
class ProductReview(models.Model):
    customer = models.ForeignKey(cmodels.Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(gmodels.Stock,on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    review = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.customer.fullname + self.product.product.title