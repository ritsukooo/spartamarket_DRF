from django.shortcuts import render
from rest_framework.views import APIView
from .models import Product
from rest_framework.response import Response
from .serializers import ProductsSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class ProductListAPIView(APIView):

    

    def get(self, request):  # -------------------상품목록 조회--------------------------#

        produts = Product.objects.all()
        serializer = ProductsSerializer(produts, many=True)
        return Response(serializer.data)

    def post(self, request):  # ---------------------상품 등록-----------------------------#
        
        permission_classes = [IsAuthenticated]

        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetailAPIView(APIView):
    def get(self, request, product_pk):  # ---------------------상품 상세 조회-----------------------------#
        product = get_object_or_404(Product, pk=product_pk)
        serializer = ProductsSerializer(product)
        return Response(serializer.data)

    def put(self, request, product_pk):  # ---------------------상품 수정-----------------------------#

        permission_classes = [IsAuthenticated]

        product = get_object_or_404(Product, pk=product_pk)
        if product.author == request.user:
            serializer = ProductsSerializer(
                product, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response("수정 권한 없음", status=status.HTTP_401_UNAUTHORIZED)

    # ---------------------상품 삭제-----------------------------#

    def delete(self, request, product_pk):

        permission_classes = [IsAuthenticated]

        product = get_object_or_404(Product, pk=product_pk)
        if product.author == request.user:
            product.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response("삭제 권한 없음", status=status.HTTP_401_UNAUTHORIZED)
