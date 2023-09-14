#Routers and viewsets... 

from rest_framework import viewsets,mixins

from . models import Product
from . serializers import ProductSerializer

#VIEWSETS  
class ProductViewSet(viewsets.ModelViewSet):
    """
    get -> list -> Queryset
    get -> retrieve -> product instance Detail view
    post -> create -> New instance
    put -> Update 
    patch -> PArtial Update
    delete -> destroy
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk' #default  
    
class ProductGenericViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    get -> list ->Queryset. 
    get -> retrieve -> Product Instance detail. 
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    
product_list_view = ProductGenericViewSet.as_view({'get':'list'})
product_detail_view = ProductGenericViewSet.as_view({'get':'retrieve'})
    
    
    