from rest_framework import serializers
from admin_app.models import *


class MainCateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategories
        fields = '__all__'

class CityNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityName
        fields = '__all__'

class ResourceLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceLanguage
        fields = '__all__'
        
class ResourceTypeSerializer(serializers.ModelSerializer):
    main_categories = MainCateSerializer(read_only=True)
    
    class Meta:
        model = ResourceType
        fields = ['id','main_categories','name']
        
class ResourceFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceField
        fields = '__all__'
        
class BookFilterSerialiazer(serializers.ModelSerializer):
    city_name_of_book = CityNameSerializer(read_only=True)
    resource_language_book = ResourceLanguageSerializer(read_only=True)
    
    class Meta:
        model = Books
        fields = ['id','name_book','author_book','description','publisher_year','city_name_of_book','resource_language_book',]

class BookSerializer(serializers.ModelSerializer):
    resource_type_book = ResourceTypeSerializer(read_only=True)
    city_name_of_book = CityNameSerializer(read_only=True)
    resource_language_book = ResourceLanguageSerializer(read_only=True)
    resource_field_book = ResourceTypeSerializer(read_only=True)
    
    class Meta:
        model = Books
        fields = ['id','name_book','author_book','description','publisher_year','resource_type_book','city_name_of_book','resource_language_book','file','image','resource_field_book','publisher_name','ISBN_code','institution_that_added_resource','institution_where_the_thesis_was_submitted','protection_institution','magazine','page_number',]
        
        
class BookDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadBooks
        fields = '__all__'
        
    
class CreateDownloadBook(serializers.ModelSerializer):
    
    class Meta:
        model = DownloadBooks
        fields = '__all__'
        
    def create(self, validated_data):
        craete = DownloadBooks.objects.create(
            book = self.context.get('get_book'),
            author = self.context.get('user'),
            download_date = validated_data.get('download_date')
        )
        return craete
    
    

class CreateBookSerializer(serializers.ModelSerializer):
    
    
    class  Meta:
        model = Books
        fields = ['file','image','name_book','author_book','city_name_of_book','resource_language_book','resource_type_book','resource_field_book','publisher_name','publisher_year','ISBN_code','institution_that_added_resource','institution_where_the_thesis_was_submitted','protection_institution','magazine','description','page_number','created_at',]
        
    def create(self, validated_data):
        create = Books.objects.create(
            author = self.context.get('user'),
            name_book = validated_data['name_book'],
            author_book = validated_data['author_book'],
            publisher_name = validated_data['publisher_name'],
            publisher_year = validated_data['publisher_year'],
            ISBN_code = validated_data['ISBN_code'],
            institution_that_added_resource = validated_data['institution_that_added_resource'],
            institution_where_the_thesis_was_submitted = validated_data['institution_where_the_thesis_was_submitted'],
            protection_institution = validated_data['protection_institution'],
            magazine = validated_data['magazine'],
            description = validated_data['description'],
            page_number = validated_data['page_number'],
            city_name_of_book = validated_data['city_name_of_book'],
            resource_language_book = validated_data['resource_language_book'],
            resource_type_book = validated_data['resource_type_book'],
            resource_field_book = validated_data['resource_field_book'],
            file = self.context.get('file'),
            image = self.context.get('image')
        )
        return create


class CreatePostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fieslds = ['__all__']
        
    def create(self, validated_data):
        return super(CreatePostSerializers, self).create(validated_data)