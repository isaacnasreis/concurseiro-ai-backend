import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("GOOGLE_API_KEY não encontrada no arquivo .env")
    exit(1)

client = genai.Client(api_key=api_key)

print("Modelos disponíveis:")
print("-" * 50)
try:
    for m in client.models.list():
        if 'generateContent' in m.supported_actions:
            print(f"Nome: {m.name}")
            print(f"Descrição: {m.description}")
            print("-" * 50)
except Exception as e:
    print(f"Erro ao listar modelos: {e}")
