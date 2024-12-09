from rest_framework import serializers
from .models import AiRequests


class AiRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = AiRequests
        fields = ("request_instruction",)



# class UserInfoSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ProductModel
#         fields = ("product_name","product_description","product_price","user")
