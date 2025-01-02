import sys
import os
import json
from ollama import Client
from django.http import StreamingHttpResponse
from django.conf import settings
from .models import Message, Conversation  # Ensure to import your MongoDB models
from django.utils.timezone import now

def send_request_to_ollama(request_data, conversation: Conversation) -> StreamingHttpResponse:
    try:
        client = Client(host=f"{settings.OLLAMA_HOST}:{settings.OLLAMA_PORT}")
        
        # Initializing system and user messages
        msgs = [{"role": "system", "content": settings.OLLAMA_INIT_INSTRUCT},
                {"role": "user", "content": request_data}]
        
        # Streaming output from Ollama
        output = client.chat(model="llama3:instruct", messages=msgs, stream=True)

        def event_stream():
            # Save the user message to MongoDB (assumed to be part of the conversation)
            Message.objects.create(
                conversation=conversation,
                role='user',
                content=request_data,
                timestamp=now()
            )

            # Process each chunk and yield it to the client while saving the AI response to MongoDB
            for chunk in output:
                # Extract content from the chunk
                chunk_content = chunk['message']['content']

                # Save each chunk as part of the AI message in MongoDB
                Message.objects.create(
                    conversation=conversation,
                    role='ai',
                    content=chunk_content,
                    timestamp=now()
                )

                # Yield the chunk to the client (as a part of the streaming response)
                yield f"{json.dumps(chunk)}\n\n"

        # Create a StreamingHttpResponse and return it
        response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        return response

    except Exception as exp:
        return str(exp)  # Return the exception as a string if something goes wrong
