from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate

from . import models
from order import models as omodels
from app.views import get_navbar_cat_list  ,get_total_cart_items
from .forms import SignupForm  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token  
from django.contrib.auth import get_user_model,logout  
from django.core.mail import EmailMessage  
from django.contrib import messages
from django.http import HttpResponse  
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        email = request.POST.get('email')
        if '@' in email:
            username  = email
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.success(request,"Welcome Back")
                return redirect('index')
            else:
                messages.error(request,"Invalid Credentials")
                print("not")
                return render(request,'customer/login.html',{
                    'cat_nav':get_navbar_cat_list,
                })
        else:
            messages.error(request,"Invalid Credentials")
    return render(request,'customer/login.html',{
            'cat_nav':get_navbar_cat_list,
            'cart_total':get_total_cart_items(request)
    })
  
def signup(request):  
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':  
          
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        form_data = {
            'username':email,
            'email':request.POST['email'],
            'password1':request.POST['password1'],
            'password2':request.POST['password2']
        }
        
        form = SignupForm(form_data)
        print(form.errors)
        # print(form)
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            customer = models.Customer(user = user,fullname=fullname)
            customer.save()
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Email Verification'  
            message = render_to_string('customer/acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'tok':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.content_subtype = 'html'
            email.send()  
            return render(request, 'customer/signup.html',{
            'cat_nav':get_navbar_cat_list,
            'cart_total':get_total_cart_items(request),
                "msg":"Please confirm your email address to complete the registration"
                })   
        elif form.has_error:
            return render(request, 'customer/signup.html',{
            'cat_nav':get_navbar_cat_list,
            'errors':form.errors,
            'cart_total':get_total_cart_items(request)
            })
    return render(request, 'customer/signup.html',{
            'cat_nav':get_navbar_cat_list,
            'cart_total':get_total_cart_items(request)
            })  

def activate(request):  
    uidb64 = request.GET.get('uidb64')
    token = request.GET.get('token')
    home_url = get_current_site(request)
    message = f"Activation link is invalid! <a href='https://{home_url.domain}'>Home</a>&nbsp;<a href='https://{home_url.domain}/login'>Login</a>"
    if uidb64 and token:
        User = get_user_model()  
        try:  
            uid = force_str(urlsafe_base64_decode(uidb64))  
            user = User.objects.get(pk=uid)  
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
            user = None  
        if user is not None and account_activation_token.check_token(user, token):  
            user.is_active = True  
            user.save()  
            messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
            return redirect('login')
        else:  
            return HttpResponse(message)
    else:
          return HttpResponse(message)

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def customer_account_page(request):
    customer = models.Customer.objects.get(user=request.user)
    message = None
    error = None
    if request.method == "POST":
        if request.POST['fullname'] and len(request.POST['fullname']) > 5 and request.POST['mobile'] and len(request.POST['mobile']) > 10 and request.POST['address'] and len(request.POST['address']) > 5 and request.POST['zipcode'] and len(request.POST['zipcode']) > 4 and request.POST['province'] and len(request.POST['province']) > 0:
            customer.fullname = request.POST['fullname']
            customer.mobile_no = request.POST['mobile']
            customer.address = request.POST['address']
            customer.city = request.POST['city']
            customer.zipcode = request.POST['zipcode']
            customer.province = request.POST['province']
            customer.save()
            print("saved")
            message = "Profile Updated"
        else:
            error = "Invalid Data all fields required"
    return render(request,'customer/customer-account.html',{
        'cat_nav':get_navbar_cat_list,
        'cart_total':get_total_cart_items(request),
        'customer':customer,
        'message':message,
        'error':error
    })

@login_required(login_url='login')
def my_order_page(request):
    filter = request.GET.get('filter',None)
    customer = models.Customer.objects.get(user=request.user)
    orders = None
    if filter:
        if filter == "pending":
            orders = omodels.Order.objects.select_related().filter(check_out=True).filter(customer=customer).filter(status="pending").order_by("-id")
        elif filter == "processing":
            orders = omodels.Order.objects.select_related().filter(check_out=True).filter(customer=customer).filter(status="processing").order_by("-id")
        elif filter == "shipped":
            orders = omodels.Order.objects.select_related().filter(check_out=True).filter(customer=customer).filter(status="shipped").order_by("-id")
        elif filter == "delivered":
            orders = omodels.Order.objects.select_related().filter(check_out=True).filter(customer=customer).filter(status="delivered").order_by("-id")
        elif filter == "cancelled":
            orders = omodels.Order.objects.select_related().filter(check_out=True).filter(customer=customer).filter(status="cancelled").order_by("-id")
        elif filter == "rejected":
            orders = omodels.Order.objects.select_related().filter(check_out=True).filter(customer=customer).filter(status="rejected").order_by("-id")
        
    if orders == None:
        orders = omodels.Order.objects.select_related().filter(check_out=True).filter(customer=customer).order_by("-id")
    return render(request,'customer/my-order-page.html',{'orders':orders,'filter':filter})