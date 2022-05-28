from django.shortcuts import redirect, render
from app import models as gmodels
from customers import models as cmodels
from app.views import get_navbar_cat_list, get_total_cart_items
# from app.views import get_navbar_cat_list
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage  
from django.template.loader import render_to_string  
from django.contrib.sites.shortcuts import get_current_site  

# Create your views here.
@login_required(login_url='login')
def shopping_cart_page(request):
    customer = cmodels.Customer.objects.get(user=request.user)
    order = models.Order.objects.select_related().filter(customer=customer).filter(check_out=False)
    if len(order) > 0:
        cart_items = models.OrderItem.objects.select_related().filter(order=order[0])
        temp_price = 0
        for i in cart_items:
            total_item_price = i.product.sale_price * i.quantity
            temp_price +=get_discount(total_item_price,i.product.discount) 
        price = temp_price
        shipping_charges = models.ShippingCharges.objects.all()
        charges = shipping_charges[0]
    else:
        cart_items = None
        price = 0
        charges = 0
    return render(request,'order/cart.html',{
    'cat_nav':get_navbar_cat_list,
    'cart_items':cart_items,
    'price':price,
    'shipping_charges':charges,
    'cart_total':get_total_cart_items(request)})

@login_required(login_url='login')
def add_to_cart(request):
    if request.method == "POST":
        print("authenticated",request.user)
        stock = request.POST.get('submit',None)
        quantity = request.POST.get('quantity',None)
        size = request.POST.get('size',None)
        color = request.POST.get('color',None)
        url = request.POST.get('url-path',None)

            
        product = gmodels.Stock.objects.select_related().get(pk=stock)
        if product.quantity >= int(quantity):
            customer = cmodels.Customer.objects.get(user=request.user)
            order = models.Order.objects.select_related().filter(customer=customer).filter(check_out=False)
                
            if size == None:
                size = ""
            if color == None:
                color = ""
            if len(order) == 0:
                order = models.Order(customer=customer)
                order.save()
                order_item = models.OrderItem(product=product,order=order,quantity=quantity,color=color,size=size)
                order_item.save()
            else:
                order = order[0]
                try:
                    check_order_item = models.OrderItem.objects.get(order=order,product=product,size=size,color=color)
                    check_order_item.quantity +=int(quantity)
                    check_order_item.save()
                    print("not found")
                except:
                    order_item = models.OrderItem(product=product,order=order,quantity=quantity,color=color,size=size)
                    order_item.save()
                    print("except")
            messages.success(request,"Item Added")
        else:
            messages.error(request,f"Item Not Added only {product.quantity} left")

        # pr = product.product.title+"?id="+str(product.product.id)
        return redirect(f"/shop/{product.product.title}?id={stock}")
        
@login_required(login_url='login')
def remove_to_cart(request):
    if request.method == "POST":
        itemid = request.POST.get('item',None)
        if itemid:
            item = models.OrderItem.objects.get(pk=itemid)
            item.delete()
    return redirect('cart')

@login_required(login_url='login')
def place_order(request):
    if request.method == "POST":
        customer = cmodels.Customer.objects.get(user=request.user)
        if customer.mobile_no and len(customer.mobile_no) > 0 and customer.address and len(customer.address) > 0 and customer.city and len(customer.city) > 0 and customer.zipcode and len(customer.zipcode) > 0 and customer.province and len(customer.province) > 0:
            print(customer.zipcode)
            sub_total = request.POST.get('sub_total')
            shipping = request.POST.get('shipping')
            customer = cmodels.Customer.objects.get(user=request.user)
            order = models.Order.objects.select_related().filter(customer=customer).filter(check_out=False)
            if len(order) > 0:
                order_items = models.OrderItem.objects.select_related().filter(order=order[0])
                for item in order_items:
                    print
                    stock = gmodels.Stock.objects.get(pk=item.product.id)
                    if stock.quantity >= item.quantity:
                        stock.quantity -=item.quantity
                        stock.save()
                    else:
                        messages.error(request,"Order Not Placed")
                        print("no items available")
                        return redirect("cart")
                print(order[0])
                order[0].total_price = int(round(float(sub_total)))
                order[0].shipping_fee = shipping
                order[0].check_out = True
                order[0].save()
                print("order save",order[0].total_price)

                # Sending Email Order Placed
                
                current_site = get_current_site(request)
                mail_subject = 'Order Placed'
                message = "This email is to confirm your order has been Placed and Now it is in Pending State.We will send you another email as soon as it going to Processing.Thank you for choosing us"
                html_message = render_to_string('customer/order-placed-mail.html', {
                    'user': customer,  
                    'domain': current_site.domain,
                    'order':order[0],
                    'order_items':order_items,
                    'message': message,
                    'mail_subject':mail_subject

                })
                to_email = customer.user.email 
                email = EmailMessage(  
                            mail_subject,html_message,  to=[to_email]  ,
                )  
                email.content_subtype = 'html'
                email.send()
                messages.success(request,"Order Placed")
                return redirect("cart")
        else:
            messages.error(request,"please add complete details")
            return redirect("account")
    return redirect("cart")

@login_required(login_url='login')
def order_details(request,order=None):
    if order:
        order_details = models.Order.objects.select_related().get(order_id=order)
        order_items = models.OrderItem.objects.select_related().filter(order=order_details)
        return render(request,'order/order-details.html',{
            'order':order_details,
            'order_items':order_items
        })
    return redirect('account')

def get_discount(price,discount):
    return price - (price * discount / 100)

@login_required(login_url="login")
def update_item(request):
    if request.method == "POST":
        item = request.POST.get('item_id')
        quantity = request.POST.get('updated_quantity')
        
        if item and quantity:
            
            item_ = models.OrderItem.objects.get(pk=item)
            item_.quantity = quantity
            item_.save()
    return redirect('cart')