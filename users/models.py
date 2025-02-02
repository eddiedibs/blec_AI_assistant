import os
from datetime import datetime, timezone

from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.exceptions import ValidationError
from image_cropping import ImageCropField, ImageRatioField
from django.db.models.signals import post_save
from django.dispatch import receiver
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload  # Import this!
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

from api.utils import send_email





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

def get_existing_file_id(service, filename, folder_id):
    """Checks if a file with the same name already exists in the Drive folder."""
    query = f"name='{filename}' and '{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id)").execute()
    
    files = results.get("files", [])
    return files[0]["id"] if files else None  # Return file ID if found, else None

def upload_to_drive(file_path, filename):
    """Uploads a file to Google Drive only if it doesn't already exist."""
    credentials = service_account.Credentials.from_service_account_file(
        settings.SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    service = build("drive", "v3", credentials=credentials)

    # Check if file already exists in Drive
    existing_file_id = get_existing_file_id(service, filename, settings.FOLDER_ID)
    
    if existing_file_id:
        print(f"File already exists in Drive: {filename}")
        return f"https://drive.google.com/uc?id={existing_file_id}"  # Return existing file URL

    # If file doesn't exist, upload it
    file_metadata = {"name": filename, "parents": [settings.FOLDER_ID]}
    media = MediaFileUpload(file_path, mimetype="image/jpeg")
    
    uploaded_file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()

    # Get file ID and create public sharing permission
    file_id = uploaded_file.get("id")
    service.permissions().create(
        fileId=file_id, body={"role": "reader", "type": "anyone"}
    ).execute()

    return f"https://drive.google.com/uc?id={file_id}"

class Doctor(models.Model):
    GENDER_CHOICES = [
        ('DR.', 'DR.'),
        ('DRA.', 'DRA.'),
    ]
    name = models.CharField(max_length=100,verbose_name="Nombre y apellido")
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES, default="", verbose_name="Género")
    specialization = models.CharField(max_length=100, default="",verbose_name="Especialidad")  # e.g., "Cardiologist", "Dermatologist"
    description = models.TextField(max_length=380, default="",verbose_name="Descripción")  # e.g., "Recognized by his expertise.. etc"
    contact = models.CharField(max_length=15, blank=True, null=True, verbose_name="Número telefónico")
    email = models.EmailField(blank=True, null=True,verbose_name="Correo electrónico")
    profile_picture = models.ImageField(upload_to='doctor_profiles/', blank=True, null=True,verbose_name="Foto de perfil")
    cropping = ImageRatioField('profile_picture', '300x300')  # Crop to a 300x300 square
    drive_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Doctor"  # Singular name
        verbose_name_plural = "Doctores"  # Plural name

    def __str__(self):
        return f"{self.name} ({self.specialization})"


@receiver(post_save, sender=Doctor)
def upload_image_to_drive(sender, instance, created, **kwargs):
    """Uploads profile picture to Google Drive and updates drive_url."""
    if instance.profile_picture and not instance.drive_url:  # Only upload if there's no drive_url yet
        file_path = instance.profile_picture.path
        filename = os.path.basename(file_path)

        # Upload to Google Drive
        drive_link = upload_to_drive(file_path, filename)

        # Update the model instance with the Google Drive URL
        instance.drive_url = drive_link
        instance.save(update_fields=["drive_url"])

class PatientParent(models.Model):
    name = models.CharField(max_length=200, default="",verbose_name="Nombre y apellido")
    id_number = models.CharField(max_length=30, default="",verbose_name="Cédula de identidad")
    contact_phone_number = PhoneNumberField(region="VE", blank=True, null=True,verbose_name="Número telefónico de contacto")  # Change "US" as needed
    email = models.EmailField(blank=True, null=True,verbose_name="Correo electrónico")

    class Meta:
        verbose_name = "Representante"  # Singular name
        verbose_name_plural = "Representantes"  # Plural name

    def __str__(self):
        return self.name




class Patient(models.Model):
    name = models.CharField(max_length=200, default="",verbose_name="Nombre y apellido")
    birth_date = models.DateField(blank=True, null=True,verbose_name="Fecha de nacimiento")
    parent = models.ForeignKey(PatientParent, on_delete=models.CASCADE, related_name='patient_parents', default="",verbose_name="Razón de consulta")

    class Meta:
        verbose_name = "Paciente"  # Singular name
        verbose_name_plural = "Pacientes"  # Plural name

    def __str__(self):
        return self.name
    
    @property
    def age(self):
        # Convert string to datetime object
        birthdate = datetime.fromisoformat(str(self.birth_date))

        # Get the current date (UTC)
        today = datetime.now(timezone.utc).date()

        # Calculate the full difference
        delta = today - birthdate.date()

        if delta.days < 30:
            return f"{delta.days} día(s)"
        elif delta.days < 365:
            months = delta.days // 30  # Approximate months
            return f"{months} mes(es)"
        else:
            years = delta.days // 365  # Approximate years
            return f"{years} año(s)"
    
class Appointment(models.Model):
    STATUS_CHOICES = [
            ('Pendiente', 'Pendiente'),
            ('Agendada', 'Agendada'),
            ('Cancelada', 'Cancelada'),
        ]


    class Meta:
        verbose_name = "Cita médica"  # Singular name
        verbose_name_plural = "Citas médicas"  # Plural name

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments', verbose_name="Doctor")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments', verbose_name="Paciente")
    appointment_date = models.DateTimeField(verbose_name="Fecha de cita médica")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pendiente', verbose_name="Estado")
    appointment_reason = models.TextField(blank=True, null=True , verbose_name="Razón de consulta")

    def save(self, *args, **kwargs):
        is_new_instance = self.pk is None  # Check if it's a new instance
        previous_status = None

        if not is_new_instance:
            previous_status = Appointment.objects.get(pk=self.pk).status

        super().save(*args, **kwargs)  # Save the instance first

        # Send email only if the status has changed to "Agendada"
        if (is_new_instance or previous_status != self.status) and self.status == "Agendada":
            send_scheduled_email(self)

    class Meta:
        # unique_together = ('doctor', 'appointment_date')  # Prevent overlapping appointments
        ordering = ['appointment_date']  # Default ordering

    def __str__(self):
        return f"Appointment with {self.doctor.name} for {self.patient.name} on {self.appointment_date}"


    @property
    def date_formatted(self):
        # Convert string to datetime object
        date_obj = datetime.fromisoformat(str(self.appointment_date))

        # Dictionary for month names in Spanish
        months_es = {
            1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
            5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
            9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
        }

        # Extract date components
        day = date_obj.day
        month = months_es[date_obj.month]
        year = date_obj.year
        hour = date_obj.hour
        minute = date_obj.minute

        # Format hour in 12-hour format with AM/PM
        am_pm = "AM" if hour < 12 else "PM"
        hour = hour % 12 or 12  # Convert 0 to 12

        # Format minute with leading zero if necessary
        minute_str = f"{minute:02d}"

        # Return formatted date string
        return f"{day} de {month} del {year} a las {hour}:{minute_str}{am_pm}"

def send_scheduled_email(appointment):
    """Helper function to send email when an appointment is scheduled."""
    patient = appointment.patient
    parent = appointment.patient.parent
    doctor = appointment.doctor  # Assuming doctor has an email field
    retrieved_user = User.objects.all().first()

    email_body = {
        "parent": {
            "id": parent.id,
            "name": parent.name,
            "id_number": parent.id_number,
            "contact_phone_number": str(parent.contact_phone_number.as_national),
            "email": parent.email,
        },
        "patient": {
            "id": patient.id,
            "name": f"{patient.name}",
            "birth_date": patient.birth_date,
            "age": patient.age,

        },
        "appointment": {
            "id": appointment.id,
            "date": appointment.date_formatted,
            "reason": appointment.appointment_reason,
            "doctor": doctor.name,
            "doctor_email": doctor.email,
            "doctor_description": doctor.description,
            "doctor_gender": doctor.gender,
            "doctor_specialty": doctor.specialization,
            "doctor_img_src": doctor.drive_url,
        },
    }

    to_emails = [parent.email, doctor.email, retrieved_user.email]

    send_email(settings.EMAIL_HOST_USER, to_emails,"📅 ¡Tu cita médica ha sido agendada! ✅😊",email_body, "scheduled_email_template.html")
