from django.shortcuts import render
from rest_framework.views import APIView
from .models import Product
from rest_framework.response import Response
from .serializers import ProductsSerializer


# Create your views here.
class ProductListAPIView(APIView):
    def get(self,request):                                #-------------------상품목록 조회--------------------------#
        produts = Product.objects.all()
        serializer = ProductsSerializer(produts, many=True)
        return Response(serializer.data)
        