from rest_framework import generics, permissions, status
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.mail import send_mail
from .serializers import UserSerializer, PhotoSerializer
from django.shortcuts import render
from .models import Photo
from django.contrib.auth.hashers import check_password
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)


        token['email'] = user.email
        token['id'] = user.id
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['id'] = user.id


        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            user_data = {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "token": access_token,
                "registration_date": user.date_joined.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            }

            return Response({
                "user": user_data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')



class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            user_data = {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "token": access_token,
            }

            return Response({
                "message": "Login successful",
                "user": user_data,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        new_password = request.data.get('new_password')

        user = User.objects.filter(email=email).first()
        if user:
            user.set_password(new_password)
            user.save()
            return render(request, 'reset_password.html', {'message': 'Password reset successful'})
        else:
            return render(request, 'reset_password.html', {'message': 'User not found'})

    def get(self, request, *args, **kwargs):
        return render(request, 'reset_password.html') 

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        user = self.request.user

        if not user.is_authenticated:
            return Response({'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(old_password, user.password):
            return Response({'message': 'Invalid old password'}, status=status.HTTP_401_UNAUTHORIZED)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return render(request, 'change_password.html')

class PhotoUploadView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        data = {
            'message': 'Photo uploaded successfully',
            'photo': response.data,
        }

        return Response(data, status=response.status_code)

        
class UpdatePhotoView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        
        csrf_token = get_token(request)
        
        return Response({'message': 'Logout successful', 'csrf_token': csrf_token}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return render(request, 'logout.html')

class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user 

        user_data = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "last_login": user.last_login.strftime('%Y-%m-%dT%H:%M:%S.%f%z') if user.last_login else None,
            "date_joined": user.date_joined.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
        }

        return render(request, 'current_user.html', {'user_data': user_data})

            



class GetUserByIdView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = get_user_model().objects.filter(id=user_id).first()

        if user:
            user_data = {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }

            return Response({"user": user_data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

