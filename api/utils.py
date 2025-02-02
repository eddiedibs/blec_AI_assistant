import os
import json
import base64
from datetime import datetime, timezone

from jinja2 import Environment, FileSystemLoader, TemplateNotFound, TemplateError
from ollama import Client
from django.http import StreamingHttpResponse
from django.conf import settings
from .models import Message, Conversation  # Ensure to import your MongoDB models
from django.utils.timezone import now
from io import BytesIO
import pycurl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings




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







def get_gmail_response(data, token_url):
    buffer = BytesIO()
    curl = pycurl.Curl()
    post_data = json.dumps(data)
    curl.setopt(curl.URL, token_url)
    curl.setopt(curl.POST, 1)
    curl.setopt(curl.POSTFIELDS, post_data)
    curl.setopt(curl.WRITEFUNCTION, buffer.write)

    if not data["access_token"]:
        curl.setopt(curl.HTTPHEADER, ["Content-Type: application/json"])

        curl.perform()
        curl.close()

        response = json.loads(buffer.getvalue().decode())

        if "access_token" in response:
            return response["access_token"]
        else:
            print(f"Error getting access token: {response}")
            return None

    else:
        curl.setopt(curl.HTTPHEADER, ["Content-Type: application/json", "Accept: application/json"])

        curl.perform()
        curl.close()

        response = json.loads(buffer.getvalue().decode())

        if "labelIds" in response:
            return response["labelIds"][0]
        else:
            print(f"Error getting access token: {response}")
            return None


def send_email(from_email, to_emails, subject, context, email_template):
    access_token = get_gmail_response({
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "refresh_token": settings.REFRESH_TOKEN,
        "grant_type": "refresh_token",
        "access_token": None,
        "redirect_uri": "https://developers.google.com/oauthplayground"
    }, settings.TOKEN_URL)



    # Render the email content using Jinja2 (as shown earlier)
    env = Environment(loader=FileSystemLoader("templates"))
    try:
        template = env.get_template(email_template)
    except TemplateNotFound:
        print("Error: Email template not found.")
        return

    try:
        html_content = template.render(**context)
    except TemplateError as e:
        print(f"TemplateError: {e}")
        return

    # Construct the email message
    msg = MIMEMultipart()
    msg["From"] = from_email
    if isinstance(to_emails, list):  # Check if it's a list
        msg["To"] = ", ".join(to_emails)  
    else:
        msg["To"] = to_emails  
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    # Encode the email in base64 for Gmail API
    raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    # Send the email using the Gmail API
    try:
        response = get_gmail_response({ "access_token":access_token,"raw": raw_message}, f"https://gmail.googleapis.com/gmail/v1/users/me/messages/send?access_token={access_token}")
        if response == "SENT":        
            print(f"Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")







