from re import search
from django.contrib import admin
from app import models
# Register your models here.
from django.utils.safestring import mark_safe




# @admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title','short_desc']
    list_display = ['title','short_desc','image_preview']
    filter_horizontal = ()
    list_filter = ('title','short_desc')
    fieldsets = ()
    readonly_fields = ('image_preview_inside',)

    # outside image preview
    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True

    # inside image preview
    def image_preview_inside(self, obj):
        return obj.image_preview_inside

    image_preview_inside.short_description = 'Image Preview'
    image_preview_inside.allow_tags = True
admin.site.register(models.Category, CategoryAdmin)
    

class SliderAdmin(admin.ModelAdmin):
    list_display = ['id','title','sub_title','image_preview']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    readonly_fields = ('image_preview_inside',)

    # outside image preview
    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True

    # inside image preview
    def image_preview_inside(self, obj):
        return obj.image_preview_inside

    image_preview_inside.short_description = 'Image Preview'
    image_preview_inside.allow_tags = True
admin.site.register(models.Slider,SliderAdmin)


class HeaderBannerAdmin(admin.ModelAdmin):
    list_display = ['id','show','image_preview']

    readonly_fields = ('image_preview_inside',)
    # outside image preview
    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True

    # inside image preview
    def image_preview_inside(self, obj):
        return obj.image_preview_inside

    image_preview_inside.short_description = 'Image Preview'
    image_preview_inside.allow_tags = True



    def has_add_permission(self, request):
        return models.HeaderBanner.objects.all().count()  == 0
admin.site.register(models.HeaderBanner,HeaderBannerAdmin)

class OffersAdmin(admin.ModelAdmin):
    list_display = ['title','sub_title','image_preview']
    filter_horizontal = ()
    list_filter = ('title',)
    fieldsets = ()
    readonly_fields = ('image_preview_inside',)

    # outside image preview
    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True

    # inside image preview
    def image_preview_inside(self, obj):
        return obj.image_preview_inside

    image_preview_inside.short_description = 'Image Preview'
    image_preview_inside.allow_tags = True

    def has_add_permission(self, request):
        return models.Offer.objects.all().count() < 4
admin.site.register(models.Offer,OffersAdmin)


class SubCategoryAdmin(admin.ModelAdmin):
    search_fields = ['title','category__title']
    list_display = ['title','category','image_preview']
    filter_horizontal = ()
    list_filter = ('title','category',)
    fieldsets = ()
    readonly_fields = ('image_preview_inside',)

    # outside image preview
    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True

    # inside image preview
    def image_preview_inside(self, obj):
        return obj.image_preview_inside

    image_preview_inside.short_description = 'Image Preview'
    image_preview_inside.allow_tags = True
admin.site.register(models.SubCategory,SubCategoryAdmin)

@admin.register(models.SubSubCategory)
class SubSubCategoryAdmin(admin.ModelAdmin):
    search_fields = ['title','category__title']
    list_display = ['title','category']
    filter_horizontal = ()
    list_filter = ('title','category',)
    fieldsets = ()


class BrandAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title','link','image_preview']
    filter_horizontal = ()
    list_filter = ('title',)
    fieldsets = ()
    readonly_fields = ('image_preview_inside',)

    # outside image preview
    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True

    # inside image preview
    def image_preview_inside(self, obj):
        return obj.image_preview_inside

    image_preview_inside.short_description = 'Image Preview'
    image_preview_inside.allow_tags = True
admin.site.register(models.Brand,BrandAdmin)

class SizeInLine(admin.TabularInline):
    model=models.ProductImage

class ColorInLine(admin.TabularInline):
    model=models.ProductColor

class ProductImageInLine(admin.TabularInline):
    model=models.ProductSize

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInLine,ColorInLine,SizeInLine]
    search_fields = ['title','short_desc','description','category__title','brand__title']
    list_display = ['title','category','brand','image_preview']
    filter_horizontal = ()
    list_filter = ('title','category','brand')
    fieldsets = ()
    readonly_fields = ('image_preview_inside',)

    # outside image preview
    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True

    # inside image preview
    def image_preview_inside(self, obj):
        return obj.image_preview_inside

    image_preview_inside.short_description = 'Image Preview'
    image_preview_inside.allow_tags = True
admin.site.register(models.Product,ProductAdmin)


@admin.register(models.Stock)
class StockAdmin(admin.ModelAdmin):
    search_fields = ['product__title','product__category__title']
    list_display = ['id','product','quantity','sale_price','discount','enabled']
    filter_horizontal = ()
    list_filter = ('sale_price','product__category','product__brand','product','discount','enabled',)
    fieldsets = ()
    
