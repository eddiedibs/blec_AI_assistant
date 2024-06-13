#!/home/edd1e/scripts/projs/other/aitest/venv/bin/python3

from ollama import Client
import sys
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='blec_proj/.env')
ollama_host = os.getenv('OLLAMA_HOST')
ollama_port = os.getenv('OLLAMA_PORT')
ollama_init_instruct = os.getenv('OLLAMA_INIT_INSTRUCT')


client = Client(host=f"{ollama_host}:{ollama_port}")
msgs = [{"role": "system", "content": ollama_init_instruct},
        
        {"role": "user", "content": sys.argv[1]}]
output = client.chat(model="llama3:instruct", messages=msgs, stream=True)

for chunk in output:
  content = chunk['message']['content']
  print(content, end='', flush=True)
