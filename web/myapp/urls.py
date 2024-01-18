from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    LogoutView, 
    ResetPasswordView, 
    PhotoUploadView, 
    UpdatePhotoView, 
    ChangePasswordView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('upload-photo/', PhotoUploadView.as_view(), name='upload'),
    path('update-photo/<int:pk>/', UpdatePhotoView.as_view(), name='update-photo'),
]