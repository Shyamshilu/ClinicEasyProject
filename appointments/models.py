from django.db import models
from django.contrib.auth.models import User
from doctors.models import Doctor

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Rescheduled', 'Rescheduled'),
    ]
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE)

    patient_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    reschedule_date = models.DateField(null=True, blank=True)
    reschedule_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.patient} - {self.doctor} ({self.status})"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
