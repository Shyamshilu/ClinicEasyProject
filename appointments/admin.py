from .models import Appointment
from django.contrib import admin
from .models import ContactMessage

admin.site.register(ContactMessage)
@admin.register(Appointment)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'patient_name',
        'doctor',
        'appointment_date',
        'appointment_time',
        'status',
    )

    list_filter = ('status', 'appointment_date', 'doctor')
    search_fields = ('patient_name', 'email')
