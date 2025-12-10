import google.generativeai as genai
import os

# Configura tu API Key aquí
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("¡Error! La variable de entorno GEMINI_API_KEY no está cargada.")

genai.configure(api_key=GEMINI_API_KEY)
print("Listando modelos disponibles...")
for m in genai.list_models():
    # Filtramos solo los que sirven para generar contenido (texto/chat)
    if 'generateContent' in m.supported_generation_methods:
        print(f"- {m.name}")