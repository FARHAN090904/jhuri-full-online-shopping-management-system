from django.urls import path
from .views import LoginView, RegisterView, ProfileView, AddAddressView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('add-address/', AddAddressView.as_view()),
 path('send-otp/',      views.send_otp,      name='send-otp'),
    path('verify-otp/',    views.verify_otp,    name='verify-otp'),
    path('reset-password/', views.reset_password, name='reset-password'),
path('change-password/', views.change_password, name='change-password'),
]
