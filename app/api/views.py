from . import serializer
from rest_framework.decorators import api_view,permission_classes
from .. import models
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import filters
from .pagination import StockListPagination
from review import models as rmodels
from review.api.serializer import ProductReviewSerializer
@api_view(['GET'])
@permission_classes([AllowAny])
def get_Categories(request):

    cat_qs = models.Category.objects.all()
    cat_serialized_data = serializer.CategorySerializer(cat_qs,many=True)

    sub_cat_qs = models.SubCategory.objects.all()
    sub_serialized_data = serializer.SubCategorySerializer(sub_cat_qs,many=True)

    sub_sub_cat_qs = models.SubSubCategory.objects.all()
    sub_sub_serialized_data = serializer.SubSubCategorySerializer(sub_sub_cat_qs,many=True)
    
    catlist = []
    for cat in cat_serialized_data.data:
        sublist = []
        for sub_cat in sub_serialized_data.data:
            if sub_cat['category'] == cat['id']:
                subsublist = []
                for subsub_cat in sub_sub_serialized_data.data:
                    if sub_cat['id'] == subsub_cat['category']:
                        subsublist.append(subsub_cat)
                sublist.append({'sub':sub_cat,'subsublist':subsublist})
        catlist.append({'cat':cat,"sub_list":sublist})
    return Response(catlist)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_home(request):
    # main categories
    cat_qs = models.Category.objects.order_by('?').all()
    catserializer = serializer.CategorySerializer(cat_qs,many=True)
    # subcategories
    subcat_qs = models.SubCategory.objects.order_by('?').all() [:18]
    subcatserializer = serializer.SubCategorySerializer(subcat_qs,many=True)
    # slider 
    slider_qs = models.Slider.objects.order_by('?').all()
    sliderserializer = serializer.SliderSerializer(slider_qs,many=True)
    # brands
    brands_qs = models.Brand.objects.order_by('?').all()[:12]
    brandserailizer = serializer.BrandSerializer(brands_qs,many=True)
    # offers 
    offers_qs = models.Offer.objects.order_by('?').all()
    offerserializer = serializer.OfferSerializer(offers_qs,many=True)
    # stock
    stock_qs = models.Stock.objects.filter(enabled=True).order_by('?')[:40]
    stockserializer = serializer.StockSerializer(stock_qs,many=True)
    # stock
    stock_best_qs = models.Stock.objects.filter(enabled=True).order_by('?')[:15]
    stockbestserializer = serializer.StockSerializer(stock_best_qs,many=True)
    
    res = {
        'slider':sliderserializer.data,
        'categories':catserializer.data,
        'subcat':subcatserializer.data,
        'brand':brandserailizer.data,
        'offer':offerserializer.data,
        'best_sellers':stockbestserializer.data,
        'products':stockserializer.data
    }
    return Response(res)

@permission_classes([AllowAny])
class List_Stock_Search(generics.ListAPIView):
    search_fields = ['product__title','=product__category__title','=product__category__category__title','=product__category__category__category__title','=product__brand__title']
    filter_backends = (filters.SearchFilter,)
    queryset = models.Stock.objects.filter(enabled=True).all()
    serializer_class = serializer.StockSerializer
    pagination_class = StockListPagination
    
    

    #     return queryset
    def get_queryset(self):
        order = self.request.GET.get('orderby', 'id')
        if order:
            new_context = models.Stock.objects.filter(
                enabled=True,
            ).order_by(order)
        else:
            new_context = models.Stock.objects.filter(
                enabled=True,
            ).order_by("-id")

        return new_context

    def get_context_data(self, **kwargs):
        context = super(List_Stock_Search, self).get_context_data(**kwargs)
        order = self.request.GET.get('orderby', 'id')
        if order:
            context['orderby'] = order
        else:
            context['orderby'] = '-id'

        return context

@api_view(['GET'])
@permission_classes([AllowAny])
def get_single_product(request,id=None):
    print(id)
    if id:
        stock_qs = models.Stock.objects.get(id=id)
        stock_serialized = serializer.StockSerializer(stock_qs,many=False)
        similar_products = models.Stock.objects.filter(product__brand=stock_qs.product.brand).order_by('?')[:12]
        similar_serialized = serializer.StockSerializer(similar_products,many=True)
        product_images_qs = models.ProductImage.objects.filter(product=stock_qs.product)
        product_images_serializer = serializer.ProductImageSerializer(product_images_qs,many=True)
        color_qs = models.ProductColor.objects.filter(product=stock_qs.product)
        color_serializer = serializer.ProductColorSerializer(color_qs,many=True)
        size_qs = models.ProductSize.objects.filter(product=stock_qs.product)
        size_serializer = serializer.ProductSizeSerializer(size_qs,many=True)
        review_qs = rmodels.ProductReview.objects.filter(product=stock_qs)
        review_serializer = ProductReviewSerializer(review_qs,many=True)
        
        res = {
            'stock':stock_serialized.data,
            'images':product_images_serializer.data,
            'colors':color_serializer.data,
            'sizes':size_serializer.data,
            'reviews':review_serializer.data,
            'similar':similar_serialized.data
        }
        return Response(res)



    

