from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site  
from ..token import account_activation_token  
from customers.forms import SignupForm
from ..models import Customer
from .serializer import CustomerSerializer, UserSerializer
from rest_framework import generics
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from django.template.loader import render_to_string  
from django.utils.encoding import force_bytes  
from django.utils.http import urlsafe_base64_encode  
from django.core.mail import EmailMessage  
from rest_framework.decorators import api_view


def signup_user(request):  
    if request.method == 'POST':  
        res = {}
        res['error']=False
        res['message']=""
        try:
            fullname = request.POST.get('fullname')
            email = request.POST.get('email')
            print(email)
            form_data = {
                'username':email,
                'email':request.POST['email'],
                'password1':request.POST['password1'],
                'password2':request.POST['password2']
            }
            
            form = SignupForm(form_data)
            print(form.errors)
            if form.is_valid():  
                # save form in the memory not in database  
                user = form.save(commit=False)  
                user.is_active = False  
                user.save()  
                customer = Customer(user = user,fullname=fullname)
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
                res['message'] = "We have sent an Verification Link to your email. Verify Email Address"
                return JsonResponse(res,safe=False)
            elif form.has_error:
                res['error'] = True
                res['message'] = "All Fields Required"
                return JsonResponse(res,safe=False)
        except:
            res['error'] = True
            res['message'] = "All Fields Required"
            return JsonResponse(res,safe=False)
     
#Login User and Get Token
class CutomAuthToken(ObtainAuthToken):
    permission_classes = [permissions.AllowAny ]
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created =Token.objects.get_or_create(user=user)
        customer_qs = Customer.objects.get(user=user)
        serialized_data = CustomerSerializer(customer_qs,many=False)
        return Response({
            'token':token.key,
            'customer':serialized_data.data
        }) 
@api_view(['POST'])
def saveUserDetails(request,id=None):
    if request.method == "POST":
        if id:
            try:
                customer = Customer.objects.get(pk=id)
            except:
                customer = None
            if customer is not None:
                customer.fullname = request.POST['fullname']
                customer.mobile_no = request.POST['mobile']
                customer.address = request.POST['address']
                customer.city = request.POST['city']
                customer.zipcode = request.POST['zipcode']
                customer.province = request.POST['province']
                customer.save()
                return Response({'error':False,'message':'data updated'})
