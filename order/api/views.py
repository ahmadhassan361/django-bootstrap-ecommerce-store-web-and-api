from rest_framework.decorators import api_view
from rest_framework.response import Response
from app import models as gmodels
from customers import models as cmodels
from order.views import get_discount
from .. import models
from . import serializer
from django.core.mail import EmailMessage  
from django.template.loader import render_to_string  
from django.contrib.sites.shortcuts import get_current_site  

@api_view(['POST'])
def add_item_to_cart(request):
    if request.method == "POST":
        stock = request.POST.get('stock_id', None)
        quantity = request.POST.get('quantity', None)
        size = request.POST.get('size', None)
        color = request.POST.get('color', None)
        customer_id = request.POST.get('customer_id', None)
        if customer_id:
            product = gmodels.Stock.objects.get(pk=stock)
            if product.quantity >= int(quantity):
                customer = cmodels.Customer.objects.get(id=customer_id)
                order = models.Order.objects.filter(
                    customer=customer).filter(check_out=False)
                if size == None:
                    size = ""
                if color == None:
                    color = ""
                if len(order) == 0:
                    order = models.Order(customer=customer)
                    order.save()
                    order_item = models.OrderItem(
                        product=product, order=order, quantity=quantity, color=color, size=size)
                    order_item.save()
                else:
                    order = order[0]
                    try:
                        check_order_item = models.OrderItem.objects.get(
                            order=order, product=product, size=size, color=color)
                        check_order_item.quantity += int(quantity)
                        check_order_item.save()
                    except:
                        order_item = models.OrderItem(
                            product=product, order=order, quantity=quantity, color=color, size=size)
                        order_item.save()
                messages = "item added"
                error = False
            else:
                messages = f"item not added only {product.quantity} left"
                error = True
        return Response({
            'message': messages,
            'error': error
        })

@api_view(['GET'])
def get_cart_items(request):
    if request.method == "GET":
        id = request.GET.get("id", None)
        res = {
            'message': "not authorized",
            'error': True,
            'items': [],
            'price': 0.0,
            'shipping_charges': 0
        }
        if id:
            customer = cmodels.Customer.objects.get(id=id)
            order = models.Order.objects.filter(
                customer=customer).filter(check_out=False)
            if len(order) > 0:
                cart_items = models.OrderItem.objects.filter(order=order[0])
                cart_items_serialized = serializer.OrderItemSerializer(
                    cart_items, many=True)
                temp_price = 0
                for i in cart_items:
                    total_item_price = i.product.sale_price * i.quantity
                    temp_price += get_discount(total_item_price,
                                               i.product.discount)
                price = temp_price
                shipping_charges = models.ShippingCharges.objects.last()
                shipping_charges_serializer = serializer.ShippingChargesSerializer(
                    shipping_charges, many=False)
                res['items'] = cart_items_serialized.data
                res['price'] = price
                res['shipping_charges'] = shipping_charges_serializer.data['charges']
                res['error'] = False
                res['message'] = 'cart items'
            else:
                res['items'] = []
                res['price'] = 0.0
                res['shipping_charges'] = 0
                res['error'] = False
                res['message'] = 'no items in cart'
        return Response(res)

@api_view(['POST'])
def place_order(request):
    if request.method == "POST":
        id = request.POST.get('customer_id', None)
        res = {
            'error': False,
            'message': 'order placed successfully'
        }
        if id:
            customer = cmodels.Customer.objects.get(id=id)
            sub_total = request.POST.get('sub_total')
            shipping = request.POST.get('shipping')
            order = models.Order.objects.select_related().filter(
                customer=customer).filter(check_out=False)
            if len(order) > 0:
                order_items = models.OrderItem.objects.select_related().filter(
                    order=order[0])
                error = False
                for item in order_items:
                    stock = item.product
                    if stock.quantity >= item.quantity:
                        pass
                    else:
                        error = True

                if error == False:
                    for item in order_items:
                        stock = item.product
                        if stock.quantity >= item.quantity:
                            stock.quantity -= item.quantity
                            stock.save()

                    print(order[0])
                    order[0].total_price = int(round(float(sub_total)))
                    order[0].shipping_fee = shipping
                    order[0].check_out = True
                    order[0].save()
                    print("order save", order[0].total_price)

                    # Sending Email Order Placed

                    current_site = get_current_site(request)
                    mail_subject = 'Order Placed'
                    message = "This email is to confirm your order has been Placed and Now it is in Pending State.We will send you another email as soon as it going to Processing.Thank you for choosing us"
                    html_message = render_to_string('customer/order-placed-mail.html', {
                        'user': customer,
                        'domain': current_site.domain,
                        'order': order[0],
                        'order_items': order_items,
                        'message': message,
                        'mail_subject': mail_subject

                    })
                    to_email = customer.user.email
                    email = EmailMessage(
                        mail_subject, html_message,  to=[to_email],
                    )
                    email.content_subtype = 'html'
                    email.send()
                    return Response(res)
                else:
                    res['error'] = True
                    res['message'] = 'some items quantity not available'
                    return Response(res)
@api_view(['POST'])
def update_item(request):
    res = {
        'error':False,
        'message':'item updated'
    }
    if request.method == "POST":
        item = request.POST.get('item_id')
        quantity = request.POST.get('updated_quantity')
        if item and quantity:
            item_ = models.OrderItem.objects.get(pk=item)
            item_.quantity = quantity
            item_.save()
            return Response(res)
    res['error']=True
    res['message'] = "something went wrong"
    return Response(res)

@api_view(['POST'])
def remove_to_cart(request):
    res = {
        'error':False,
        'message':'item removed'
    }
    if request.method == "POST":
        itemid = request.POST.get('item_id',None)
        if itemid:
            item = models.OrderItem.objects.get(pk=itemid)
            item.delete()
            return Response(res)
    res['error']=True
    res['message'] = "something went wrong"
    return Response(res)

@api_view(['GET'])
def my_order_page(request):
    filter = request.GET.get('filter',None)
    id = request.GET.get('customer_id',None)
    if id:
        customer = cmodels.Customer.objects.get(pk=id)
        orders = None
        if filter:
            if filter == "pending":
                orders = models.Order.objects.select_related().filter(check_out=True).filter(customer=customer).filter(status="pending").order_by("-id")
            elif filter == "processing":
                orders = models.Order.objects.select_related().filter(check_out=True).filter(customer=customer).filter(status="processing").order_by("-id")
            elif filter == "shipped":
                orders = models.Order.objects.select_related().filter(check_out=True).filter(customer=customer).filter(status="shipped").order_by("-id")
            elif filter == "delivered":
                orders = models.Order.objects.select_related().filter(check_out=True).filter(customer=customer).filter(status="delivered").order_by("-id")
            elif filter == "cancelled":
                orders = models.Order.objects.select_related().filter(check_out=True).filter(customer=customer).filter(status="cancelled").order_by("-id")
            elif filter == "rejected":
                orders = models.Order.objects.select_related().filter(check_out=True).filter(customer=customer).filter(status="rejected").order_by("-id")
            
        if orders == None:
            orders = models.Order.objects.select_related().filter(check_out=True).filter(customer=customer).order_by("-id")
        serialized_order = serializer.OrderSerializer(orders,many=True)
        return Response(serialized_order.data)
@api_view(['GET'])
def order_details(request,):
    id = request.GET.get('id',None)
    if id:
        order_details = models.Order.objects.get(pk=id)
        serialized_order = serializer.OrderSerializer(order_details,many=False)
        order_items = models.OrderItem.objects.filter(order=order_details)
        order_items_serialized = serializer.OrderItemSerializer(order_items, many=True)
        return Response({
            'order':serialized_order.data,
            'order_items':order_items_serialized.data
        })

