from django.db import models
from django.contrib.auth.models import User

class MainCategories(models.Model):
    name= models.CharField(max_length=150)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Asosiy Kategoriya"
        verbose_name_plural = "Asosiy Kategoriya"

class CityName(models.Model):
    name= models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Davlat nomi"
        verbose_name_plural = "Davlat nomi"

class ResourceLanguage(models.Model):
    name= models.CharField(max_length=150)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Resurs tili"
        verbose_name_plural = "Resurs tili"
    
class ResourceType(models.Model):
    name= models.CharField(max_length=150)
    main_categories = models.ForeignKey(MainCategories, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Resurs turi"
        verbose_name_plural = "Resurs turi"
    
class ResourceField(models.Model):
    name= models.CharField(max_length=150)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Resurs sohasi"
        verbose_name_plural = "Resurs sohasi"


class Books(models.Model):
    file = models.FileField(upload_to='file', blank=False, null=False)
    image = models.ImageField(upload_to = 'media', blank=False, null=False)
    name_book = models.CharField(max_length=150,blank=False, null=False)
    author_book = models.CharField(max_length=150,blank=False, null=False)
    city_name_of_book = models.ForeignKey(CityName, on_delete=models.CASCADE)
    resource_language_book = models.ForeignKey(ResourceLanguage, on_delete=models.CASCADE) 
    resource_type_book = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    resource_field_book = models.ForeignKey(ResourceField, on_delete=models.CASCADE)
    publisher_name = models.CharField(max_length=150,blank=False, null=False)
    publisher_year = models.IntegerField(default=1990)
    ISBN_code = models.CharField(max_length=150,blank=False, null=False)
    institution_that_added_resource = models.CharField(max_length=150,blank=False, null=False) #Resursni qo'shgan muassasa
    institution_where_the_thesis_was_submitted = models.CharField(max_length=150,blank=False, null=False) #Dissertatsiyani qo'shgan muassasa
    protection_institution = models.CharField(max_length=150,blank=False, null=False) #Himoya muassasasi:
    magazine = models.CharField(max_length=150,blank=False, null=False) #Jurnal
    description = models.TextField(default='No description')
    page_number = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField()
    
    def __str__(self):
        return self.name_book

    class Meta:
        verbose_name = "Kitoblar"
        verbose_name_plural = "Kitoblar"
    
class DownloadBooks(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE,null=True,blank=True)
    author = models.ForeignKey(User,  on_delete=models.CASCADE,null=True,blank=True)
    download_date = models.DateField()
    
    def __str__(self):
        return f"{self.book__name_book}"

    class Meta:
        verbose_name = "Yuklab olingan kitoblar"
        verbose_name_plural = "Yuklab olingan kitoblar"
    
    