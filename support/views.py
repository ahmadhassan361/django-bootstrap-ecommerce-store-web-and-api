from django.shortcuts import render
from django.contrib import messages

from app.views import get_navbar_cat_list,get_total_cart_items
from . import models
# Create your views here.
def contact_page(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        if name and email and subject and message:
            obj = models.Contact(name=name,email=email,subject=subject,message=message)
            obj.save()
            messages.success(request,"your message successfully sent")
    return render(request,'support/contact.html',{
            'cat_nav':get_navbar_cat_list,
            'cart_total':get_total_cart_items(request),
            'contact':True
    })

def faq_page(request):
    questions = models.FAQ.objects.all()
    return render(request,'support/faq-page.html',{
            'cat_nav':get_navbar_cat_list,
            'cart_total':get_total_cart_items(request),
            'questions':questions
    })

def refund_policy_page(request):
    return render(request,'support/refund-policy.html',{
        'cat_nav':get_navbar_cat_list,
            'cart_total':get_total_cart_items(request)
    })

def privacy_policy_page(request):
    return render(request,"support/privacy-policy.html",{
        'cat_nav':get_navbar_cat_list,
            'cart_total':get_total_cart_items(request),
    })
def about_us_page(request):
    return render(request,"support/about.html",{
        'cat_nav':get_navbar_cat_list,
            'cart_total':get_total_cart_items(request),
    })

