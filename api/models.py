import mongoengine as me
import uuid
from django.utils.timezone import now
from django.conf import settings  # Import settings for user reference

class AiRequests(me.Document):
    user_id = me.IntField(required=True)  # Use IntegerField
    request_instruction = me.StringField(max_length=400, required=True)

    def __str__(self):
        return f"Request: {self.request_instruction}"


class Conversation(me.Document):
    meta = {'collection': 'conversation'}  # Explicit MongoDB collection name
    
    user_id = me.IntField(required=True)  # User identifier
    created_at = me.DateTimeField(default=now)
    updated_at = me.DateTimeField(default=now)
    conversation_id = me.StringField(max_length=255, unique=True, required=True)  # Unique conversation identifier

    def __str__(self):
        return f"Conversation {self.conversation_id} with User ID {self.user_id}"


class Message(me.Document):
    meta = {'collection': 'message'}  # Explicit MongoDB collection name

    ROLE_CHOICES = ('user', 'ai')  # MongoEngine enum equivalent

    conversation = me.ReferenceField(Conversation, reverse_delete_rule=me.CASCADE, required=True)
    role = me.StringField(choices=ROLE_CHOICES, required=True)  # 'user' or 'ai'
    content = me.StringField(required=True)  # The message text
    timestamp = me.DateTimeField(default=now)  # When the message was sent

    def __str__(self):
        return f"Message by {self.role} at {self.timestamp}"
