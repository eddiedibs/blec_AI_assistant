# from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from PIL import Image
from uuid import uuid4

from djongo import models
from django.utils.timezone import now




class AiRequests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_instruction = models.TextField(max_length=400)
    

    def __str__(self):
        return f"request: {self.request_instruction}"


class Conversation(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)  # Unique ID for the user (e.g., user identifier)
    created_at = models.DateTimeField(default=now)  # Timestamp of when the conversation started
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp of the last message
    conversation_id = models.CharField(max_length=255, unique=True)  # Unique identifier for the conversation

    def __str__(self):
        return f"Conversation {self.conversation_id} with User Of ID {self.user_id}"


class Message(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('ai', 'AI'),
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)  # 'user' or 'ai'
    content = models.TextField()  # The message text
    timestamp = models.DateTimeField(default=now)  # When the message was sent

    def __str__(self):
        return f"Message by {self.role} at {self.timestamp}"
