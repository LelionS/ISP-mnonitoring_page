from django.urls import path
from . import views

urlpatterns = [
     path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home, name='home'),
    path('verify-otp/<str:email>/', views.otp_verify, name='otp_verify'),
    path('logout/', views.logout_view, name='logout'),
]
