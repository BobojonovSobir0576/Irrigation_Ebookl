from rest_framework import serializers
from admin_app.models import *

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'
        
class BookDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadBooks
        fields = '__all__'
        
    
class CreateDownloadBook(serializers.ModelSerializer):
    
    class Meta:
        model = DownloadBooks
        fields = '__all__'
        
    def create(self, validated_data):
        print(self.context.get('get_book'))
        print(self.context.get('user'))
        craete = DownloadBooks.objects.create(
            book = self.context.get('get_book'),
            author = self.context.get('user'),
            download_date = validated_data.get('download_date')
        )
        return craete
