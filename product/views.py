from rest_framework import authentication, generics,mixins,permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from . models import Product
from . serializers import ProductSerializer
from . permissions import IsStaffEditorPermission

"""
USING GENERICS..  
"""
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 
    # authentication_classes = [
    #     authentication.SessionAuthentication,
    #     authentication.TokenAuthentication
    #     ]
    # permission_classes = [IsStaffEditorPermission]
    
    #For additional and custom create method .. 
    def perform_create(self, serializer):
        #  serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        
        if content is None:
            content = title  
        serializer.save(user=self.request.user, content=content)

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
    
class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
    
    def perform_update(self, serializer):
        instance = serializer.save()
        return instance
        # if not serializer.content:
        #     instance.content = instance.title 
            
    
product_update_view = ProductUpdateAPIView.as_view()

class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
    
    def perform_destroy(self, instance):
        #instance
        super().perform_destroy(instance)
    
product_destroy_view = ProductDestroyAPIView.as_view()

"""
CLASS BASED VIEW -Mixin. (the diff- with function based view is ins class based view
do not write conditions for the method
we only write function for request method.)
"""
class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin, #gives ability to access methods build in the mixin. 
    mixins.RetrieveModelMixin, #has method for retrieving data by passing a PK
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field = 'pk'  
    # authentication_classes = [authentication.SessionAuthentication]
    # permission_classes = [IsStaffEditorPermission]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly] 
    # permission_classes = [permissions.DjangoModelPermissions] #When decid using djangoMP
    
    def get(self, request, *args, **kwargs):
        # print("Maduka pcm the coder... ")
        print(args,kwargs)
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
product_mixin_view = ProductMixinView.as_view()

"""
USING APIView
"""
@api_view(["GET","POST"])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method 
    if method == "GET":
        if pk is not None:
            # specific view.
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data) 
        #All list view. 
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)
    
        ######## this function is to be used in generic view for getting data for a logged in user.
        # def get_queryset(self, *args, **kwargs):
        #     request = self.request    # this is used in view not in serializer (request.context.get())
        #     if not user.is_authenticated:
        #           return Product.objects.none()
        #     print(request.user)
        #     qs = super().get_queryset(*args, **kwargs)
        #     return super().get_queryset(*args, **kwargs)
        #  or return qs.filter(user=request.user)
    
    if method == "POST": 
        # create item.. 
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.pop('email')
            print(email)
            
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None 
            price = serializer.validated_data.get('price')
            
            if content is None:
                content = title 
            serializer.save(user=request.user, content=content)
            print(serializer.data)
            return Response(serializer.data)
        return Response({"invalid":"not good data"}, status=400)

