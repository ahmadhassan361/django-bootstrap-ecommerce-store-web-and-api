from statistics import mode
from django.contrib import admin
from . import models
# Register your models here.


class OrderItemLine(admin.TabularInline):
    model = models.OrderItem
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


class OrderAdmin(admin.ModelAdmin):
    search_fields = ['order_id', 'customer__fullname',
                     'customer__user__username', 'status', 'date']
    inlines = [OrderItemLine]
    list_display = ['order_id', 'customer', 'date', 'status','get_city','get_zipcode']
    list_editable = ['status']
    filter_horizontal = ()
    list_filter = ('order_id','date','status','customer__city','customer__zipcode')
    fieldsets = ()
    readonly_fields = ('check_out','customer')
    list_per_page = 25
    @admin.display(ordering='customer__city', description='City')
    def get_city(self, obj):
        return obj.customer.city
    @admin.display(ordering='customer__zipcode', description='Zipcode')
    def get_zipcode(self, obj):
        return obj.customer.zipcode

    def save_model(self, request, obj, form, change):
        print(form.changed_data)
        if 'status' in form.changed_data:
            send_email_order_update(request, instance=obj)
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        return qs.filter(check_out=True)


admin.site.register(models.Order, OrderAdmin)


def send_email_order_update(request, instance):
    from .models import OrderItem
    from django.core.mail import EmailMessage
    from django.template.loader import render_to_string
    from django.contrib.sites.shortcuts import get_current_site

    order = instance
    mail_subject = ""
    message = ""
    if instance.status == "processing":
        mail_subject = "Order Confirmed"
        message = "This email is to confirm your order has been Confirmed. We will send you another email as soon as it going to shipped"

    elif instance.status == "shipped":
        mail_subject = "Order Shipped"
        message = "This email is to confirm your order has been Shipped. We will send you another email as soon as it going to Delivered"

    elif instance.status == "delivered":
        mail_subject = "Order Delivered"
        message = "This email is to confirm your order has been delivered. Thank you for choosing us"
    elif instance.status == "cancelled":
        mail_subject = "Order Cancelled"
        message = f"This email is to confirm your order has been cancelled.\nReason: {order.cancel_reason}"
    elif instance.status == "rejected":
        mail_subject = "Order Rejected"
        message = f"This email is to confirm your order has been rejected.\nReason: {order.cancel_reason}"
    else:
        mail_subject = "Order Placed"
        message = f"This email is to confirm your order has been Placed and Now it is in Pending State.We will send you another email as soon as it going to Processing.Thank you for choosing us"
    current_site = get_current_site(request)
    order_items = OrderItem.objects.filter(order=order)
    html_message = render_to_string('customer/order-placed-mail.html', {
        'user': order.customer,
        'domain': current_site.domain,
        'order': order,
        'order_items': order_items,
        'message': message,
        'mail_subject':mail_subject
    })
    to_email = order.customer.user.email
    email = EmailMessage(
        mail_subject, html_message, to=[to_email],
    )
    email.content_subtype = 'html'
    # email.send()
    print("email sended")


class ShippingChargesAdmin(admin.ModelAdmin):
    list_display = ['id', 'charges']

    def has_add_permission(self, request):
        return models.ShippingCharges.objects.all().count() == 0
