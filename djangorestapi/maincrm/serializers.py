from django.contrib.auth.models import User
from .models import Customer
from rest_framework import serializers

"""
User Serializers
"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
        
class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'is_staff')

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user   

class DetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_staff')

"""
Customer Serializers
"""

class ListCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name')

class CreateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['created_by_user', 'last_modified_by_user']

class DetailCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'surname', 'photo', 'created_by_user', 'last_modified_by_user')
