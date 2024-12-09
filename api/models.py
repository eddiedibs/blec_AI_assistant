from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from PIL import Image





class AiRequests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_instruction = models.TextField(max_length=400)
    

    def __str__(self):
        return f"request: {self.request_instruction}"

