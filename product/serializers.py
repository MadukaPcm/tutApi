from rest_framework import serializers
from rest_framework.reverse import reverse
from . models import Product
from . import validators
from api.serializers import UserPublicSerializer

class ProductSerializer(serializers.ModelSerializer):
    # user = UserPublicSerializer(read_only=True)
    owner = UserPublicSerializer(source = 'user', read_only=True)
    my_user_data = serializers.SerializerMethodField(read_only=True)
    my_discount = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)  #Dealing with links.. .. 
    edit_url = serializers.SerializerMethodField(read_only=True)
    # hyp_url = serializers.HyperlinkedIdentityField(
    #     view_name='product-details',
    #     lookup_field='pk'
    # )
    email = serializers.EmailField(write_only=True)
    
    """Custom validation by calling a from validators file """
    title = serializers.CharField(validators=[validators.validate_title_no_hello,validators.unique_product_title])
    
    class Meta:     
        model = Product
        fields = [
            'owner',
            'url',
            'edit_url',
            # 'hyp_url',
            'id',
            'email',
            'title',
            'price',
            'content',
            'sale_price',
            'my_discount',
            'my_user_data',
        ]
    
    def get_my_user_data(self, obj):
        if obj.user:
            return {"username":obj.user.username}
        else:
            return {"username":None}
        
    """Custom validation using function within the serializer."""
    
    # def validate_title(self, value):
    #     request = self.context.get('request')
    #     user = request.user 
        
    #     qs = Product.objects.filter(user=user, title__iexact=value)  # it shouldl be unique,. 
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already a product name")
    #     return value   
    
    #On adding addition email field.. we override the default method.
    # def create(self, validated_data):
    #     # return Product.objects.create(**validated_data)
    #     if 'email' in validated_data:
    #         email = validated_data.pop('email')
    #         obj = super().create(validated_data)
    #         print(email,obj)
    #     else:
    #         raise serializers.ValidationError("Email is required !!")
    #     return obj
    
    # def update(self, instance, validated_data):
    #     if 'email' in validated_data:
    #         email = validated_data.pop('email')
    #         obj = super().update(instance,validated_data)
    #     else:
    #         raise serializers.ValidationError("Email is required !!")
    #     return obj
    
    
    def get_edit_url(self,obj):
        # return f"api/product/v2/{obj.pk}/retrieve/"
        request = self.context.get('request')
        if request is None:
            return None 
        return reverse("product-edit", kwargs={"pk":obj.pk}, request=request)
        
    def get_url(self,obj):
        # return f"api/product/v2/{obj.pk}/retrieve/"
        request = self.context.get('request')
        if request is None:
            return None 
        return reverse("product-details", kwargs={"pk":obj.pk}, request=request)
    
    def get_my_discount(self,obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Product):
            return None 
        return obj.get_discount()