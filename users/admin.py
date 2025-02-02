from django.contrib import admin
from users.models import Doctor, Patient, Appointment, PatientParent
from image_cropping import ImageCroppingMixin

@admin.register(Doctor)
class DoctorAdmin(ImageCroppingMixin, admin.ModelAdmin):
    exclude = ('drive_url',)
    list_display = ['name', 'specialization', 'contact', 'email']
    search_fields = ['name', 'specialization']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'age']
    search_fields = ['name']

@admin.register(PatientParent)
class PatientParentAdmin(admin.ModelAdmin):
    list_display = ['name', 'id_number', 'contact_phone_number', 'email']
    search_fields = ['name']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'patient', 'appointment_date', 'status']
    list_filter = ['appointment_date', 'doctor', 'status']
    search_fields = ['doctor__name', 'patient__name']
