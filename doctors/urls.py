from django.urls import path
from . import views
from doctors import views

urlpatterns = [
    path("doctor/dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
    path('doctors/', views.doctor_list, name='doctors'),
    path('add-doctors/', views.add_doctors),
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
]
