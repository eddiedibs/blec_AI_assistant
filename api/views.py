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


from .serializers import AiRequestSerializer, DoctorModelSerializer#,ChatFormModelSerializer
from .utils import send_request_to_ollama
from .models import Conversation, Message, AiRequests
from users.models import Doctor


class AiRequestView(APIView):
    serializer_class = AiRequestSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()


        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            request_instruction = serializer.data.get("request_instruction")
            # user_id = serializer.data.get("user")  # Assuming 'user' is passed in the payload
            
            # user = serializer.data.get("user")
            # retrieved_user = User.objects.filter(id=user).first()
            # Retrieve or create the user
            user = User.objects.all().first()
            if not user:
                return Response({'Bad Request': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            # Create or retrieve a conversation
            conversation, created = Conversation.objects.get_or_create(
                user_id=user.id,
                defaults={'conversation_id': str(uuid4()), 'created_at': now()}
            )

            # data_obj = send_request_to_ollama(
            #     request_data="If and ONLY IF we had a previous conversation related to doctor appointment data. Return that data with a json object containing the following structure with no other comments: {'doctor':'doctorName','patient':'patientName', 'patienIdNumber':'patientIdNumber','patientPhoneNumber':'patientPhoneNumber'}.", 
            #     conversation=conversation, 
            #     return_stream=False,  
            #     )

            # # Send request to Ollama and stream the response
            # print(data_obj)
            return send_request_to_ollama(request_data=request_instruction, conversation=conversation, content_instruct=settings.OLLAMA_INIT_INSTRUCT)
            # return Response(AiRequestSerializer(ai_request).data, status=status.HTTP_201_CREATED)
        else:
            return Response({'Bad Request': 'Something went wrong...'}, status=status.HTTP_400_BAD_REQUEST)



# class AiRequestView(APIView):
#     serializer_class = AiRequestSerializer

#     def post(self, request, format=None):
#         if not self.request.session.exists(self.request.session.session_key):
#             self.request.session.create()


#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             request_instruction = serializer.data.get("request_instruction")
#             # user_id = serializer.data.get("user")  # Assuming 'user' is passed in the payload
            
#             # user = serializer.data.get("user")
#             # retrieved_user = User.objects.filter(id=user).first()
#             # Retrieve or create the user
#             user = User.objects.all().first()
#             if not user:
#                 return Response({'Bad Request': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

#             # Create or retrieve a conversation
#             conversation, created = Conversation.objects.get_or_create(
#                 user_id=user.id,
#                 defaults={'conversation_id': str(uuid4()), 'created_at': now()}
#             )

#             # data_obj = send_request_to_ollama(
#             #     request_data="If and ONLY IF we had a previous conversation related to doctor appointment data. Return that data with a json object containing the following structure with no other comments: {'doctor':'doctorName','patient':'patientName', 'patienIdNumber':'patientIdNumber','patientPhoneNumber':'patientPhoneNumber'}.", 
#             #     conversation=conversation, 
#             #     return_stream=False,  
#             #     )

#             # # Send request to Ollama and stream the response
#             # print(data_obj)
#             return send_request_to_ollama(request_data=request_instruction, conversation=conversation, content_instruct=settings.OLLAMA_INIT_INSTRUCT)
#             # return Response(AiRequestSerializer(ai_request).data, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'Bad Request': 'Something went wrong...'}, status=status.HTTP_400_BAD_REQUEST)


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