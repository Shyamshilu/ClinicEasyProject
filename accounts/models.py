from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True)
    gender = models.CharField(max_length=10)
    blood_group = models.CharField(max_length=5)
    phone = models.CharField(max_length=15,null=True)
    address = models.TextField()

    def __str__(self):
        return self.name

class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    specialty = models.CharField(max_length=100, blank=True, null=True)  

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class Registration(models.Model):
    patientname = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    bloodgroup = models.CharField(max_length=5)
    mobile = models.CharField(max_length=10)
    email = models.EmailField()
    address = models.TextField()
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.patientname
