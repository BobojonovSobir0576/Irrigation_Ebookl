from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import AuthenticationFailed

from admin_app.models import *

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserLoginSerializers(serializers.ModelSerializer):
    username = serializers.CharField(max_length=250)
    
    class Meta:
        model = User
        fields = ['username','password']

        
class UserPorfilesSerializers(serializers.ModelSerializer):
    groups = GroupSerializer(read_only=True, many=True)
    
    class Meta:
        model = User
        fields = ['username','groups','first_name','last_name',]
        
        
class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        get_groups = Group.objects.get(name = 'Student')
        create = User.objects.create(
            password = make_password(validated_data.get('password')),
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        create.groups.add(get_groups)
        create.save()

        return create
        
    def update(self,instance,validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.set_password(validated_data.get('password', instance.username))
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance