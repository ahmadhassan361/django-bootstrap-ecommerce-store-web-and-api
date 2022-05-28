from atexit import register
from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','email','subject','contact_date']
    filter_horizontal = ()
    list_filter = ('name','email','contact_date')
    fieldsets = ()

@admin.register(models.FAQ)
class FAQAdmin(admin.ModelAdmin):
    search_fields = ['question']
    list_display = ['question']
    filter_horizontal = ()
    list_filter = ('question',)
    fieldsets = ()