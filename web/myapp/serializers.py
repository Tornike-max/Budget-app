from rest_framework import serializers
from .models import CustomUser, Photo


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'repeat_password')

    def validate(self, data):
        if data.get('password') != data.get('repeat_password'):
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('repeat_password', None) 
        user = CustomUser.objects.create_user(**validated_data, password=password)
        return user

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'image')
