from math import prod
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from customers import models as cmodels
from app import models as gmodels
from . import models
# Create your views here.

@login_required(login_url='login')
def add_review(request):
    if request.method == "POST":
        rating = request.POST.get('rate',None)
        review = request.POST.get('review',None)
        stock_id = request.POST.get('stock',None)
        url = request.POST.get('url',None)


        customer = cmodels.Customer.objects.get(user=request.user)
        product = gmodels.Stock.objects.get(pk=stock_id)
        reviews = models.ProductReview.objects.filter(customer=customer).filter(product=product)
        if len(reviews) <=0:
            if rating and review and customer and product:
                review = models.ProductReview(customer=customer,product=product,rating=rating,review=review)
                review.save()
    return redirect(url)



