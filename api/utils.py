import sys
import os
import json

from ollama import Client
from django.http import StreamingHttpResponse

from django.conf import settings



def send_request_to_ollama(request_data) -> object:
    try:

        client = Client(host=f"{settings.OLLAMA_HOST}:{settings.OLLAMA_PORT}")
        msgs = [{"role": "system", "content": settings.OLLAMA_INIT_INSTRUCT},
                
                {"role": "user", "content": request_data}]
        output = client.chat(model="llama3:instruct", messages=msgs, stream=True)

        def event_stream():
            for chunk in output:
                # content = chunk['message']['content']
                yield f"{json.dumps(chunk)}\n\n"
                
        response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        return response

    except Exception as exp:
        return exp