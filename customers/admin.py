from statistics import mode
from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['user__email','fullname','mobile_no','city''zipcode']
    list_display = ['id','user','fullname','mobile_no','city','zipcode']
    filter_horizontal = ()
    list_filter = ('user__email','fullname','mobile_no','city','zipcode')
    fieldsets = ()