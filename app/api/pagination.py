from rest_framework.pagination import PageNumberPagination

class StockListPagination(PageNumberPagination):
    page_size = 20
    

