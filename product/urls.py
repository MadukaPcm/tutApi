from django.urls import path
from . import views
from product.viewsets import product_list_view,product_detail_view

urlpatterns = [
    path('', views.product_alt_view, name="product-detail"), #ProductListCreateAPIView ::product_alt_view is all in!
    path('<int:pk>/update/', views.product_update_view, name="product-edit"),
    path('<int:pk>/delete/', views.product_destroy_view),
    path('<int:pk>/', views.product_alt_view), #ProductDetailAPIView
    #Using class view Mixin.. 
    path('mixin/', views.product_mixin_view),  
    path('v2/', product_list_view),
    path('v2/<int:pk>/retrieve/', product_detail_view, name="product-details"),
]   