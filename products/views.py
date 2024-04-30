from django.shortcuts import render
from rest_framework.views import APIView
from .models import Product
from rest_framework.response import Response
from .serializers import ProductsSerializer
from rest_framework import status


# Create your views here.
class ProductListAPIView(APIView):
    def get(self,request):                                                #-------------------상품목록 조회--------------------------#
        produts = Product.objects.all()
        serializer = ProductsSerializer(produts, many=True)
        return Response(serializer.data)
    
    

    def post(self,request):                                               #---------------------상품 등록-----------------------------#
        serializer = ProductsSerializer(data =request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED) 
        
        
        
        