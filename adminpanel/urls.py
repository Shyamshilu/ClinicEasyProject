from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('users/', views.admin_users, name='admin_users'),
    path('users/add/', views.admin_add_user, name='admin_add_user'),
    path('users/edit/<int:user_id>/', views.admin_edit_user, name='admin_edit_user'),
    path('users/delete/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
    path('patients/', views.admin_patients, name='admin_patients'),
    path('patients/add/', views.admin_add_patient, name='admin_add_patient'),
    path('patients/edit/<int:patient_id>/', views.admin_edit_patient, name='admin_edit_patient'),
    path('patients/delete/<int:patient_id>/', views.admin_delete_patient, name='admin_delete_patient'),
    path('appointments/', views.admin_appointments, name='admin_appointments'),
    path('appointments/add/', views.admin_add_appointment, name='admin_add_appointment'),
    path('doctors/', views.admin_doctors, name='admin_doctors'),
    path('doctors/add/', views.admin_add_doctor, name='admin_add_doctor'),
    path('appointments/export-excel/', views.export_appointments_excel, name='export_appointments_excel'),
    path('doctors/edit/<int:doctor_id>/', views.admin_edit_doctor, name='admin_edit_doctor'),
    path('doctors/delete/<int:doctor_id>/', views.admin_delete_doctor, name='admin_delete_doctor'),
    path("admin/appointments/",views.admin_appointments, name="admin_appointments"),
    path("admin/appointments/delete/<int:id>/", views.admin_delete_appointment, name="admin_delete_appointment"),
    path("feedback/", views.admin_feedback, name="admin_feedback"),

]

