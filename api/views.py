import json
import requests

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.models import User

from .serializers import AiRequestSerializer
from .models import AiRequests
from .utils import send_request_to_ollama
    
class AiRequestView(APIView):
    serializer_class = AiRequestSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()


        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            request_instruction = serializer.data.get("request_instruction")
            # user = serializer.data.get("user")
            # retrieved_user = User.objects.filter(id=user).first()
        
            # ai_response_text = send_request_to_ollama(request_instruction)
            ai_response_stream = send_request_to_ollama(request_instruction)

            # print(ai_response_text)

            # ai_request = AiRequests(
            #                     request_instruction=ai_response_text,
            #                     user=User.objects.all().first(),
            #                     )
            # ai_request.save()

            return ai_response_stream
            # return Response(AiRequestSerializer(ai_request).data, status=status.HTTP_201_CREATED)
        else:
            return Response({'Bad Request': 'Something went wrong...'}, status=status.HTTP_400_BAD_REQUEST)






# class ProductsDestroyView(generics.DestroyAPIView):
#     allowed_methods = ['DELETE']

#     queryset = ProductModel.objects.all()
#     serializer_class = ListProductSerializer
    
# class ProductsUpdateView(generics.UpdateAPIView):
#     allowed_methods = ['PUT']

#     queryset = ProductModel.objects.all()
#     serializer_class = ListProductSerializer