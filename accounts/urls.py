from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from . views import login_redirect,register

urlpatterns = [
    path('', views.home, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('service-details/', views.service_details, name='service-details'),
    path('contact/', views.contact, name='contact'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/',views.register,name='register'),
    path('login-redirect/', login_redirect, name='login_redirect'),
]
