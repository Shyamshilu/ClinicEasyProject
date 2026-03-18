from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    location = models.CharField(max_length=100,default='Rajkot')   # ✅ ADD THIS LINE
    experience = models.IntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='doctors/', default='assets/img/health/doctor-default.webp')

    def __str__(self):
        return self.name

class DoctorSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor.name} | {self.date} | {self.start_time}"


class Review(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['doctor', 'user']  # prevent duplicate review

    def __str__(self):
        return f"{self.user.username} - {self.doctor.name}"