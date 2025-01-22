from rest_framework import serializers
from .models import AiRequests
from users.models import Doctor, Patient
from django.utils.timezone import now

class AiRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = AiRequests
        fields = ("request_instruction",)


class DoctorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'contact', 'email']



class PatientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'id_number', 'email', 'date_of_birth']

class AppointmentSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100, trim_whitespace=True)
    last_name = serializers.CharField(max_length=100, trim_whitespace=True)
    id_number = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    birth_date = serializers.DateTimeField()
    appointment_date = serializers.DateTimeField()
    doctor = serializers.CharField(max_length=100)
    appointment_reason = serializers.CharField(max_length=500)


    def validate_appointment_date(self, value):
        if value < now():
            raise serializers.ValidationError("The appointment date cannot be in the past.")
        return value


    def create(self, validated_data):
        # Logic to save the appointment (e.g., in a database)
        # Replace this with your model logic, e.g., Appointment.objects.create(**validated_data)
        return validated_data
# class UserInfoSerializer(serializers.ModelSerializer):

#     class Meta:   
#         model = ProductModel
#         fields = ("product_name","product_description","product_price","user")
