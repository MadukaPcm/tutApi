from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.forms.models import model_to_dict
from product.models import Product
import json

#DRF. 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.serializers import ProductSerializer

#The api call function without DRF
"""
def api_home(request, *args, **kwargs):
    model_data = Product.objects.all().order_by("?").first()
    # model_data = Product.objects.get(id=3)
    data = {}
    if model_data:
        # data["id"] = model_data.id 
        # data["title"] = model_data.title
        # data["content"] = model_data.content
        # data["price"] = model_data.price
        
        #Serialization converting model instance to dictionary. 
        #using django library.... model_to_dict 
        data = model_to_dict(model_data, fields=['id','title'])#add fields,specifying fields.
    return JsonResponse(data)    
"""

@api_view(["GET","POST"])
def api_home(request, *args, **kwargs):
    instance = Product.objects.all().order_by("?").first()
    # model_data = Product.objects.get(id=4)
    # data = {}
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        print(serializer.data)
        return Response(serializer.data) 
    # if data: 
    #     print(data)
    # if instance:
    #     # data["id"] = model_data.id 
    #     # data["title"] = model_data.title
    #     # data["content"] = model_data.content
    #     # data["price"] = model_data.price
        
    #     #Serialization converting model instance to dictionary. 
    #     #using django library.... model_to_dict 
    #     # data = model_to_dict(model_data, fields=['id','title','price'])#add fields
    #     data = ProductSerializer(instance).data
    return Response({"Invalid": "not good data"}, status=400)    