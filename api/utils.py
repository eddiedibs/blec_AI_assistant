import sys
import os
import json
from ollama import Client
from django.http import StreamingHttpResponse
from django.conf import settings
from .models import Message, Conversation  # Ensure to import your MongoDB models
from django.utils.timezone import now

def send_request_to_ollama(
    request_data, 
    conversation: Conversation, 
    return_stream=True,
    content_instruct=None
) -> object:  # Return type can be StreamingHttpResponse or str
    try:
        client = Client(host=f"{settings.OLLAMA_HOST}:{settings.OLLAMA_PORT}")

        # Retrieve the conversation history from MongoDB
        # conversation_history = Message.objects.filter(conversation=conversation).order_by("timestamp")
        msgs = []
        if content_instruct:
            # Prepare the messages for the Ollama API request
            msgs = [{"role": "system", "content": content_instruct}]

        # Append the conversation history to msgs
        # for message in conversation_history:
        #     role_mapping = {"user": "user", "ai": "assistant"}  # Map roles to Ollama's expected roles
        #     role = role_mapping.get(message.role)

        #     if not role:
        #         raise ValueError(f"Invalid role '{message.role}' in conversation history")

        #     msgs.append({
        #         "role": role,
        #         "content": message.content
        #     })

        # Add the new user message to the conversation
        msgs.append({"role": "user", "content": request_data})

        # Streaming output from Ollama
        output = client.chat(model="llama3:instruct", messages=msgs, stream=True)

        if return_stream:
            # Define the streaming response
            def event_stream():
                # Save the user message to MongoDB
                Message.objects.create(
                    conversation=conversation,
                    role='user',
                    content=request_data,
                    timestamp=now()
                )

                # Process each chunk and yield it to the client while saving the AI response to MongoDB
                ai_message_content = ""
                for chunk in output:
                    chunk_content = chunk['message']['content']
                    ai_message_content += chunk_content
                    yield f"{json.dumps(chunk)}\n\n"

                # Save the full AI message to MongoDB
                if ai_message_content:
                    Message.objects.create(
                        conversation=conversation,
                        role='ai',
                        content=ai_message_content,
                        timestamp=now()
                    )

            # Return a StreamingHttpResponse
            return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

        else:
            # Collect the full AI response as a single string
            ai_message_content = ""
            for chunk in output:
                chunk_content = chunk['message']['content']
                ai_message_content += chunk_content

            # Save the user message to MongoDB
            Message.objects.create(
                conversation=conversation,
                role='user',
                content=request_data,
                timestamp=now()
            )

            # Save the full AI message to MongoDB
            if ai_message_content:
                Message.objects.create(
                    conversation=conversation,
                    role='ai',
                    content=ai_message_content,
                    timestamp=now()
                )

            # Return the full AI response as a string
            return ai_message_content

    except ValueError as ve:
        return str(ve)  # Handle specific validation errors
    except Exception as exp:
        return str(exp)  # Handle general exceptions

