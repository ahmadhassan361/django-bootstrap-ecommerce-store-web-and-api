from django.shortcuts import redirect, render
from . import models
from customers import models as cmodels
from order import models as omodels
from review import models as rmodels
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect  
from django.contrib.auth.decorators import login_required

# Create your views here.
def index_page(request):
    categories = models.SubCategory.objects.select_related().order_by('?').all()[:12]
    sliders = models.Slider.objects.all()
    trendy_products = models.Stock.objects.filter(enabled=True).select_related().order_by('?')[:12]
    new_products = models.Stock.objects.filter(enabled=True).select_related().order_by('product__date')[:12]
    cheap_products = models.Stock.objects.filter(enabled=True).select_related().order_by('sale_price')[:20]
    header_banner = models.HeaderBanner.objects.filter(show=True).last
    brands = models.Brand.objects.all()
    offers = models.Offer.objects.all()

    return render(request,'app/index.html',
    {
        'index':True,
        'index_navbar':True,
        'slider':sliders,
        'cat_nav':get_navbar_cat_list,
        'categories':categories,
        'trendy_product':trendy_products,
        'new_product':new_products,
        'brands':brands,
        'offers':offers,
        'cart_total':get_total_cart_items(request),
        'products_price':cheap_products,
        'header_banner':header_banner
    })

def shop_page(request):
    brand = request.GET.get('brand',None)
    main_cat = request.GET.get('main-cat',None)
    search = request.GET.get('search',None)
    cat = request.GET.get('cat',None)
    if main_cat:
        try:
            maincat = models.SubCategory.objects.get(pk=main_cat)
            products_list = models.Stock.objects.select_related().filter(enabled=True).filter(product__category__category=maincat).order_by('product__category__id')
        except:
            products_list = models.Stock.objects.select_related().filter(enabled=True)
    else:
        
        if search:
            print(search)
            products_list =  models.Stock.objects.select_related().filter(enabled=True).filter(Q(product__title__icontains=search) | Q(product__description__icontains=search)).select_related().order_by('product__date')
        elif brand:
            try:
                brand_ = models.Brand.objects.get(pk=brand)
                products_list = models.Stock.objects.select_related().filter(enabled=True).filter(product__brand=brand_).order_by('-id')
            except:
                products_list = models.Stock.objects.select_related().filter(enabled=True)

        else:
            if cat:
                print(cat)
                try:
                    category = models.SubSubCategory.objects.get(pk=cat)
                    products_list = models.Stock.objects.select_related().filter(enabled=True).filter(product__category=category)
                except:
                    products_list = models.Stock.objects.select_related().filter(enabled=True)
                
            else:
                products_list = models.Stock.objects.select_related().filter(enabled=True)
            
    paginator = Paginator(products_list, 20)
    page = request.GET.get('page', 1)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    data = {
        'shop':True,
        'cat_nav':get_navbar_cat_list,
        'cart_total':get_total_cart_items(request),
        'products':products,
        'search':search
    }
    if cat:
        data['cat']= category
    if main_cat:
        data['main_cat']=maincat
    if brand:
        data['brand']=brand_

    return render(request,'app/shop.html',data)

def product_details_page(request,pr=None):
    id = request.GET.get('id',None)
    add_review = None
    if id:
        try:
            product = models.Stock.objects.select_related().get(pk=id)
            images = models.ProductImage.objects.select_related().filter(product=product.product)
            products_list = models.Stock.objects.select_related().filter(enabled=True).filter(product__category__category=product.product.category.category).order_by('?')[:12]
            products_brand = models.Stock.objects.select_related().filter(enabled=True).filter(product__brand=product.product.brand).order_by('?')[:12]
            sizes = models.ProductSize.objects.select_related().filter(product=product.product)
            colors = models.ProductColor.objects.select_related().filter(product=product.product)
        except:
            return redirect('shop')
        
        if request.user.is_authenticated:
            customer = cmodels.Customer.objects.get(user=request.user)
            reviews = rmodels.ProductReview.objects.select_related().filter(customer=customer).filter(product=product)
            reviews_list = rmodels.ProductReview.objects.select_related().filter(product=product)
            if len(reviews) <= 0:
                add_review = True
        reviews_list = rmodels.ProductReview.objects.select_related().filter(product=product)
        rating = 0
        temp_rating = 0
        for i in reviews_list:
            temp_rating += i.rating
            rating = round(temp_rating / len(reviews_list))

        return render(request,'app/product-details.html',{
            'cat_nav':get_navbar_cat_list,
            'cart_total':get_total_cart_items(request),
            'stock':product,
            'images':images,
            'products':products_list,
            'products_brand':products_brand,
            'sizes':sizes,
            'colors':colors,
            'add_review':add_review,
            'reviews':reviews_list,
            'total_reviews':len(reviews_list),
            'rating':rating

        })
    return redirect('shop')

@login_required(login_url='login')
def wish_list_page(request):
    
    return render(request,'app/wish-list.html')

@login_required(login_url='admin:login')
def admin_dashboard_page(request):
    if request.user.is_staff:
        print("staff and superuser")
        
        return render(request,'admin/admin-dashboard.html')
    return redirect('index')





# Extra Functions
def get_navbar_cat_list():
    categories = models.Category.objects.select_related().all()
    subcategories = models.SubCategory.objects.select_related().all()
    subsubcategories = models.SubSubCategory.objects.select_related().all()
    cat_list = []
    for i in categories:
        temp_list = []
        for j in subcategories:
            if i == j.category:
                list_temp = []
                for k in subsubcategories:
                    if j == k.category:
                        list_temp.append(k)

                temp_list.append({
                    'sub':j,
                    'subsub':list_temp
                })
        dict = {
                "cat":i,
                "sub":temp_list
            }
        cat_list.append(dict)
    return cat_list

def get_total_cart_items(request):
    if request.user.is_authenticated:
        customer = cmodels.Customer.objects.get(user=request.user)
        order = omodels.Order.objects.select_related().filter(customer=customer).filter(check_out=False)
        if len(order) > 0:
            cart_item_num = omodels.OrderItem.objects.filter(order=order[0]).count()
        else:
            cart_item_num = 0
    else:
        cart_item_num = 0
    return cart_item_num