from django.contrib import admin
from users.models import Doctor, Patient, Appointment

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'contact', 'email']
    search_fields = ['name', 'specialization']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name','email']
    search_fields = ['first_name']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'patient', 'appointment_date', 'status']
    list_filter = ['appointment_date', 'doctor', 'status']
    search_fields = ['doctor__name', 'patient__name']
