from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import Book

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['is_staff']=user.is_staff
        # ...
        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    is_librarian = serializers.BooleanField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username','password','password2','is_librarian')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError(
                {"username": "Username already exits."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],is_staff=bool(validated_data['is_librarian'])
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username']

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'