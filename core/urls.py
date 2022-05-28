from django.contrib import admin
from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.views.decorators.csrf import csrf_exempt

# Views Import
from app import views
from support import views as support_views
from order import views as order_views
from customers import views as customer_views
from review import views as review_views
# API imports
from app.api import views as gapiviews
from order.api import views as oapiviews
from customers.api import views as capiviews
from review.api import views as rapiviews
from support.api import views as supapiviews




urlpatterns = [

    # static and media files urls
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    # admin panel urls
    path('main/dashboard', views.admin_dashboard_page,name="admindashboard"),
    path('admin/', admin.site.urls,name="admin"),

    # app urls (general)
    path('',views.index_page,name="index"),
    path('shop',views.shop_page,name="shop"),
    path('shop/<str:pr>',views.product_details_page,name="product_detail"),
    path('wishlist',views.wish_list_page,name="wishlist"),


    # Customer app urls
    path('login',customer_views.login_page,name="login"),
    path('signup',customer_views.signup,name="signup"), 
    path('logout',customer_views.logout_user,name="logout"), 
    path('activate', customer_views.activate, name='activate'), 
    path('account', customer_views.customer_account_page, name='account'), 
    path('myorder', customer_views.my_order_page, name='myorder'), 

    
    
    # Order app urls
    path('cart', order_views.shopping_cart_page, name='cart'), 
    path('add_to_cart', order_views.add_to_cart, name='add_to_cart'), 
    path('remove_to_cart', order_views.remove_to_cart, name='remove_to_cart'), 
    path('place_order', order_views.place_order, name='place_order'), 
    path('orderdetails/<int:order>', order_views.order_details, name='orderdetails'), 
    path('update_item', order_views.update_item, name='update_item'), 
    
    # support app urls
    path('contact',support_views.contact_page,name="contact"),
    path('faq',support_views.faq_page,name="faq"),
    path('policy',support_views.refund_policy_page,name="refund"),
    path('about',support_views.about_us_page,name="about"),
    path('privacy',support_views.privacy_policy_page,name="privacy"),

    # review app urls
    path('product/addreview',review_views.add_review,name="add_review"),

    #------------API Endpoints-----------
    # app api urls
    path('api/categories',gapiviews.get_Categories),
    path('api/home',gapiviews.get_home),
    path('api/products',gapiviews.List_Stock_Search.as_view()),
    path('api/single_product/<int:id>',gapiviews.get_single_product),
    # app order api urls
    path('api/add_to_cart/',oapiviews.add_item_to_cart),
    path('api/get_cart_items/',oapiviews.get_cart_items),
    path('api/place_order/',oapiviews.place_order),
    path('api/update_item/',oapiviews.update_item),
    path('api/remove_item/',oapiviews.remove_to_cart),
    path('api/my_orders/',oapiviews.my_order_page),
    path('api/order_detail/',oapiviews.order_details),
    # Customer api url
    path('api/login/', capiviews.CutomAuthToken.as_view(), name='gettoken'),
    path('api/create/', csrf_exempt(capiviews.signup_user)),
    path('api/details/<int:id>', csrf_exempt(capiviews.saveUserDetails)),
    # Review api urls
    path('api/add_review/', rapiviews.add_review),
    # Support api urls
    path('api/get_faq/', supapiviews.get_faq)



     




]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
