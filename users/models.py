from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.exceptions import ValidationError

def clean(self):
    overlapping_appointments = Appointment.objects.filter(
        doctor=self.doctor,
        date=self.date,
        start_time__lt=self.end_time,
        end_time__gt=self.start_time,
    ).exclude(id=self.id)

    if overlapping_appointments.exists():
        raise ValidationError("This appointment overlaps with another appointment.")

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(default='default.png', upload_to='profile_pics')



    def __str__(self):
        return f'{self.user.username} Profile'


    
    def save(self, *args, **kwargs):
        super().save()

        imgs = Image.open(self.img.path)

        if imgs.height > 300 or imgs.width > 300:
            output_size = (300, 300)
            imgs.thumbnail(output_size)
            imgs.save(self.img.path)

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)  # e.g., "Cardiologist", "Dermatologist"
    contact = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.specialization})"


class Patient(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Scheduled')
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.clean()  # Ensure validation is called
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('doctor', 'date', 'start_time')  # Prevent overlapping appointments
        ordering = ['date', 'start_time']  # Default ordering

    def __str__(self):
        return f"Appointment with {self.doctor.name} for {self.patient.name} on {self.date} at {self.start_time}"
