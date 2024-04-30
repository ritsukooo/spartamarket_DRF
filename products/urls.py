from . import views
from django.contrib import admin
from django.urls import path


app_name = "products"
urlpatterns = [
    path("", views.ProductListAPIView.as_view(), name="products_list"),
    path("/<int:product_pk>/", views.ProductDetailAPIView.as_view(), name="products_detail"),
    
   
]