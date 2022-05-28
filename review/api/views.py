from customers import models as cmodels
from app import models as gmodels
from .. import models
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET','POST'])
def add_review(request):
    if request.method == "POST":
        rating = request.POST.get('rate',None)
        review = request.POST.get('review',None)
        stock_id = request.POST.get('stock',None)
        customer_id = request.POST.get('customer_id',None)
        customer = cmodels.Customer.objects.get(pk=customer_id)
        product = gmodels.Stock.objects.get(pk=stock_id)
        reviews = models.ProductReview.objects.filter(customer=customer).filter(product=product)
        if len(reviews) <=0:
            if rating and review and customer and product:
                review = models.ProductReview(customer=customer,product=product,rating=int(float(rating)),review=review)
                review.save()
                return Response({
                    'error':False,
                    'message':'Your Review Added'
                })
    return Response({
                    'error':True,
                    'message':'Your Review Already Added'
                })