from django.urls import path
from accounts import views
from .views import *

urlpatterns = [
    path('doctor/dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('<int:doctor_id>/', book_appointment, name='appointment'),
    path('cancel/<int:id>/', cancel_appointment, name='cancel_appointment'),
    path('my/', my_appointments, name='my_appointments'),
    path("contact/", contact, name="contact"),
    path('reschedule/<int:id>/', reschedule_appointment, name='reschedule_appointment'),
]
