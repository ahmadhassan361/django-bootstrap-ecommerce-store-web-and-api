from django.db import models
from django.utils.safestring import mark_safe
from core.utils import compress





class Category(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to ='images/category/',default=None)
    short_desc = models.CharField(max_length=250)

    def save(self, *args, **kwargs):
                new_image = compress(self.image)
                self.image = new_image
                super().save(*args, **kwargs)

    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="120" height="120" style="border-radius: 10px;" />'.format(self.image.url))
        return ""
    @property
    def image_preview_inside(self):
        if self.image:
            return mark_safe('<img src="{}" width="200" height="200" style="border-radius: 5px;"/>'.format(self.image.url))
        return ""

    def __str__(self):
        return self.title

class SubCategory(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to ='images/sub-category/',default=None)
    def save(self, *args, **kwargs):
                new_image = compress(self.image)
                self.image = new_image
                super().save(*args, **kwargs)

    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="120" height="120" style="border-radius: 10px;" />'.format(self.image.url))
        return ""
    @property
    def image_preview_inside(self):
        if self.image:
            return mark_safe('<img src="{}" width="200" height="200" style="border-radius: 5px;"/>'.format(self.image.url))
        return ""

    def __str__(self):
        return self.category.title +" - "+self.title

class SubSubCategory(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.category) +" - "+self.title

class Brand(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to ='images/brand/')
    link = models.CharField(max_length=1000,blank=True)
    def save(self, *args, **kwargs):
                new_image = compress(self.image)
                self.image = new_image
                super().save(*args, **kwargs)
    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="120" height="120" style="border-radius: 10px;" />'.format(self.image.url))
        return ""

    @property
    def image_preview_inside(self):
        if self.image:
            return mark_safe('<img src="{}" width="200" height="200" style="border-radius: 5px;"/>'.format(self.image.url))
        return ""
    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(SubSubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    short_desc = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    new_arrival = models.BooleanField(default=False)
    image = models.ImageField(upload_to ='images/product/')
    youtube_video_url = models.CharField(max_length=1000,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
                new_image = compress(self.image)
                self.image = new_image
                super().save(*args, **kwargs)

    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="120" height="120" style="border-radius: 10px;" />'.format(self.image.url))
        return ""
    @property
    def image_preview_inside(self):
        if self.image:
            return mark_safe('<img src="{}" width="200" height="200" style="border-radius: 5px;"/>'.format(self.image.url))
        return ""
    

    def __str__(self):
        return self.title +" ("+ str(self.category) +")"

class ProductColor(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to ='images/product-color/',blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
                new_image = compress(self.image)
                self.image = new_image
                super().save(*args, **kwargs)
    def __str__(self):
        return self.title

class ProductSize(models.Model):
    size = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    def __str__(self):
        return self.size

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to ='images/product/',blank=True)
    def save(self, *args, **kwargs):
                new_image = compress(self.image)
                self.image = new_image
                super().save(*args, **kwargs)

class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    purchase_price = models.IntegerField(default=0)
    sale_price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    enabled = models.BooleanField(default=False)
    def __str__(self):
        return self.product.title +" ("+ str(self.product.category) +")"

class Slider(models.Model):
    title = models.CharField(max_length=250)
    sub_title = models.CharField(max_length=250)
    image = models.FileField(upload_to ='images/slider/',blank=True)
    def save(self, *args, **kwargs):
                new_image = compress(self.image)
                self.image = new_image
                super().save(*args, **kwargs)
    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}"  height="120" style="border-radius: 10px;" />'.format(self.image.url))
        return ""
    @property
    def image_preview_inside(self):
        if self.image:
            return mark_safe('<img src="{}" height="150" style="border-radius: 5px;"/>'.format(self.image.url))
        return ""
    def __str__(self):
        return self.title

class Offer(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100)
    image = models.ImageField(upload_to ='images/offers/',blank=True)
    def save(self, *args, **kwargs):
                new_image = compress(self.image)
                self.image = new_image
                super().save(*args, **kwargs)
    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}"  height="120" style="border-radius: 10px;" />'.format(self.image.url))
        return ""
    @property
    def image_preview_inside(self):
        if self.image:
            return mark_safe('<img src="{}"  height="200" style="border-radius: 5px;"/>'.format(self.image.url))
        return ""
    def __str__(self):
        return self.title
    
class HeaderBanner(models.Model):
    image = models.ImageField(upload_to='images/header/',blank=True)
    show = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
                new_image = compress(self.image)
                self.image = new_image
                super().save(*args, **kwargs)
    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}"   height="80" />'.format(self.image.url))
        return ""
    @property
    def image_preview_inside(self):
        if self.image:
            return mark_safe('<img src="{}"   height="60"  />'.format(self.image.url))
        return ""