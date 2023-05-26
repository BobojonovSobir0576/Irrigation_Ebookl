from django.contrib import admin
from admin_app.models import *



@admin.register(MainCategories)
class MainCategoriesAdmin(admin.ModelAdmin):
    list_display = ('name','id')
    
@admin.register(CityName)
class CityNameAdmin(admin.ModelAdmin):
    list_display = ('name','id')
    
@admin.register(ResourceLanguage)
class ResourceLanguageAdmin(admin.ModelAdmin):
    list_display = ('name','id')
    
@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ('name','main_categories','id')
    
@admin.register(ResourceField)
class ResourceFieldAdmin(admin.ModelAdmin):
    list_display = ('name','id')
    
@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('name_book','author_book','ISBN_code')
    
@admin.register(DownloadBooks)
class DownloadBooksAdmin(admin.ModelAdmin):
    list_display = ('book','author','download_date')
    
    
@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('full_name','post','download_date')