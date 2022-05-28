from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product','customer','rating','date']