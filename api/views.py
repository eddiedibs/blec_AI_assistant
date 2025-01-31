import json
import requests
from uuid import uuid4
import asyncio


from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.conf import settings


from .serializers import AiRequestSerializer, DoctorModelSerializer,AppointmentSerializer
from .utils import send_request_to_ollama
from .models import Conversation, Message, AiRequests
from users.models import Doctor, Patient, Appointment


from django.middleware.csrf import get_token
import json


def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

def validate_and_convert_data (data):
    try:
        parsed_data = json.loads(data)  # Convert string to dictionary

        # Accessing values
        message = parsed_data.get("message")
        patient = parsed_data.get("patient", {})
        appointment = parsed_data.get("appointment", {})

        # Extract specific details
        patient_name = patient.get("name")
        patient_email = patient.get("email")
        patient_birth_date = patient.get("birth_date")
        appointment_date = appointment.get("date")
        appointment_doctor = appointment.get("doctor")
        appointment_reason = appointment.get("reason")

        return {"message":message,
                "patient_name":patient_name,
                "patient_email":patient_email,
                "patient_birth_date":patient_birth_date,
                "appointment_doctor":appointment_doctor,
                "appointment_date":appointment_date,
                "appointment_reason":appointment_reason,
                }

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

class AiRequestView(APIView):
    serializer_class = AiRequestSerializer

    def post(self, request, format=None):
        # if not self.request.session.exists(self.request.session.session_key):
        #     self.request.session.create()


        request_instruction_json = request.data.get("request_instruction")

        if request_instruction_json:
            converted_data = validate_and_convert_data(request_instruction_json)

        request_instruction = f"Responde que notificarás al doctor de nombre: {converted_data['appointment_doctor']}, de su disponibilidad para la fecha: {converted_data['appointment_date']}, para la agenda de cita de l paciente de nombre: {converted_data['patient_name']}, por la razón de: {converted_data['appointment_reason']}. Comenta finalmente que una vez se coordine la cita, recibirás un mensaje mediante correo electrónico."

        # user_id = serializer.data.get("user")  # Assuming 'user' is passed in the payload
        
        # user = serializer.data.get("user")
        # retrieved_user = User.objects.filter(id=user).first()
        # Retrieve or create the user
        user = User.objects.all().first()
        if not user:
            return Response({'Bad Request': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create or retrieve a conversation
        conversation = Conversation.objects(user_id=user.id).first()

        # If not found, create a new one
        if not conversation:
            conversation = Conversation(
                user_id=user.id,
                conversation_id=str(uuid4()),  # Generate unique ID
                created_at=now()
            )
            conversation.save()  # Save to MongoDB

        return send_request_to_ollama(request_data=request_instruction, content_instruct=settings.OLLAMA_INIT_INSTRUCT, conversation=conversation)
        # return Response(AiRequestSerializer(ai_request).data, status=status.HTTP_201_CREATED)



class AiRequestAppointmentView(APIView):
    serializer_class = AppointmentSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()


        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.all().first()
            data = serializer.validated_data

            # Extract patient-related fields
            patient_data = {
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "id_number": data["id_number"],
                "email": data["email"],
                "birth_date": data["birth_date"],
            }

            # Check if the patient already exists, or create a new one
            patient, created = Patient.objects.get_or_create(
                id_number=patient_data["id_number"], defaults=patient_data
            )

            # Retrieve or create the Doctor instance
            doctor_name = data["doctor"]
            doctor = Doctor.objects.get(name=doctor_name)

            # Extract appointment-related fields
            appointment_data = {
                "appointment_date": data["appointment_date"],
                "appointment_reason": data["appointment_reason"],
                "doctor": doctor,  # Use the Doctor instance
                "status": "Pending",
            }

            # Create and save the appointment with the linked patient
            appointment, created = Appointment.objects.get_or_create(
                patient=patient,  # Link the patient instance
                status="Pending",  # Check for 'Pending' status
                defaults=appointment_data  # Provide data to create a new appointment if not found
            )

            # Update other fields in case the appointment already exists
            if not created:
                for key, value in appointment_data.items():
                    setattr(appointment, key, value)
                appointment.save()
            return Response(
                {
                    "message": "Appointment created successfully",
                    "patient": {
                        "id": patient.id,
                        "name": f"{patient.first_name} {patient.last_name}",
                        "email": patient.email,
                        "birth_date": patient.birth_date,
                    },
                    "appointment": {
                        "id": appointment.id,
                        "date": appointment.appointment_date,
                        "reason": appointment.appointment_reason,
                        "doctor": doctor.name,
                    },
                },
            status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorModelViewSet(ReadOnlyModelViewSet):  # ReadOnlyModelViewSet supports only GET requests
    queryset = Doctor.objects.all()  # Queryset for the view
    serializer_class = DoctorModelSerializer

# class ProductsDestroyView(generics.DestroyAPIView):
#     allowed_methods = ['DELETE']

#     queryset = ProductModel.objects.all()
#     serializer_class = ListProductSerializer
    
# class ProductsUpdateView(generics.UpdateAPIView):
#     allowed_methods = ['PUT']

#     queryset = ProductModel.objects.all()
#     serializer_class = ListProductSerializer