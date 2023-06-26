import json
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django.contrib.auth.models import *
from django.db.models import Q  


from admin_app.renderers import *
from admin_app.models import *
from book_app.serializers import *
from book_app.pagination import *

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework import generics, permissions, status, views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters

    
class CategoriesCountView(APIView):
    renderers = [UserRenderers]
    
    def get(self,requests):
        arr_1 = []
        for i in MainCategories.objects.all():
            book_count = Books.objects.filter(resource_type_book__main_categories = i).count()
            arr_1.append({
                'name':i.name,
                'count':book_count
              })
        return Response({'count':arr_1},status=status.HTTP_200_OK)

class BookingsListView(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookFilterSerialiazer
    filter_backends = [DjangoFilterBackend]
    filterset_fields =['name_book','author_book','city_name_of_book','resource_language_book','resource_type_book','resource_field_book','publisher_name','publisher_year',]
    
    # def get(self, request, format=None):
    #     search_name_book = request.query_params.get('search_book', '')
    #     books = Books.objects.filter((Q(author_book__icontains=search_name_book) | Q(name_book__icontains=search_name_book)))
    #     serializers = self.serializer_class(books, many=True)
    #     return Response(serializers.data, status=status.HTTP_200_OK)
    
    
class BookList(APIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = BookSerializer
    
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator
    
    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,self.request, view=self)
    
    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
    
    def get(self, request, cate_id, format=None, *args, **kwargs):
        instance = Books.objects.filter(resource_type_book__main_categories__id = cate_id)
        page = self.paginate_queryset(instance)
        print(self.paginator.page_size)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)
        return Response({'msg':serializer.data}, status=status.HTTP_200_OK)


class BookDetailViews(APIView):
    render_classes = [UserRenderers]
    
    def get(self,request,id,format=None):
        book = get_object_or_404(Books, id = id)
        serializers = BookSerializer(book)
        return Response(serializers.data,status=status.HTTP_200_OK)
    


class GetBookDownloadViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]
    
    def get(self,request,format=None):
        books = Books.objects.filter(author = request.user).order_by('-id')
        serializers = BookDownloadSerializer(books,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
    
class DownloadBooksViews(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [IsAuthenticated]

    def post(self,request,id,format=None):
        book_get = get_object_or_404(Books, id = id)
        serializers = CreateDownloadBook(data=request.data,context={'user':request.user,'get_book':book_get})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'msg':'success'},status=status.HTTP_201_CREATED)

class CreateBook(APIView):
    render_classes = [UserRenderers]
    perrmisson_class = [permissions.IsAuthenticated]

    def get(self,request,format=None):
        main_categories = MainCategories.objects.all().order_by('-id')
        cityname = CityName.objects.all().order_by('-id')
        resourceLanguage = ResourceLanguage.objects.all().order_by('-id')
        resourceType = ResourceType.objects.all().order_by('-id')
        resourceField = ResourceField.objects.all().order_by('-id')
        
        serialized_data1 = serialize("json", main_categories)
        serialized_data1 = json.loads(serialized_data1)
        
        serialized_data2 = serialize("json", cityname)
        serialized_data2 = json.loads(serialized_data2)
        
        serialized_data3 = serialize("json", resourceLanguage)
        serialized_data3 = json.loads(serialized_data3)
        
        serialized_data4 = serialize("json", resourceType)
        serialized_data4 = json.loads(serialized_data4)
        
        serialized_data5 = serialize("json", resourceField)
        serialized_data5 = json.loads(serialized_data5)
        
        return Response({'MainCategories':serialized_data1,'CityName': serialized_data2 ,'ResourceLanguage': serialized_data3 ,'ResourceType': serialized_data4  ,'ResourceField': serialized_data5 })
    
    def post(self,request,format=None):
        serializers = CreateBookSerializer(data=request.data,context = {'user':request.user,'file':request.data.get('file'),'image':request.data.get('image')})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'msg':'success'},status=status.HTTP_201_CREATED)


class CreatePostViews(APIView):
    render_classes = [UserRenderers]

    def post(self,request,fotmat=None):
        serializers = CreatePostSerializers(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'msg':'success'},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)    
        