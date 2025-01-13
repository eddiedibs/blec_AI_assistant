from rest_framework import serializers
from .models import AiRequests
from users.models import Doctor, Patient

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
        fields = ['id', 'name', 'specialization', 'contact', 'email']

class ChatFormModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'contact', 'email']


# class UserInfoSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ProductModel
#         fields = ("product_name","product_description","product_price","user")
