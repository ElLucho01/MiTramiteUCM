import os
from google import genai

# El cliente se inicializa automáticamente usando la variable de entorno GEMINI_API_KEY
if 'GEMINI_API_KEY' not in os.environ:
    raise ValueError("La variable de entorno GEMINI_API_KEY no está configurada.")

client = genai.Client()

# ¡LISTO! El modelo está listo para recibir el texto crudo del OCR
# y aplicar las instrucciones de formateo.