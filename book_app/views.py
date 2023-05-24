from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
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

class BookingsListView(generics.GenericAPIView):
    serializer_class = BookSerializer
    
    def get(self, request, format=None):
        search_name_book = request.query_params.get('search_book', '')
        books = Books.objects.filter((Q(author_book__icontains=search_name_book) | Q(name_book__icontains=search_name_book)))
        serializers = self.serializer_class(books, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

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
        instance = Books.objects.filter(resource_type_book__main_categories = cate_id)
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

        
        