import os
import time
import json
import requests
import pytesseract
from pdf2image import convert_from_path
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. CONFIGURACIÓN DE ENTORNO Y RUTAS (WINDOWS)
# ==========================================

# Configurar API Key de Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("¡Error! La variable de entorno GEMINI_API_KEY no está cargada.")

genai.configure(api_key=GEMINI_API_KEY)

# Configuración Específica de Windows para Tesseract
# Debes apuntar al ejecutable, no a la carpeta.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configuración de Poppler (Necesario para pdf2image en Windows)
# Cambia esta ruta a donde hayas descomprimido los binarios de Poppler
POPPLER_PATH = r'C:\poppler-25.12.0\Library\bin' 

# ==========================================
# 2. FUNCIONES DE EXTRACCIÓN Y PROCESAMIENTO
# ==========================================

def descargar_pdf_con_requests(url_pdf, ruta_destino):
    """
    Descarga el PDF simulando un navegador para evitar bloqueos básicos.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"⬇️ Descargando PDF desde: {url_pdf}")
    try:
        response = requests.get(url_pdf, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open(ruta_destino, 'wb') as f:
            f.write(response.content)
        print("✅ PDF descargado correctamente.")
        return True
    except Exception as e:
        print(f"❌ Error descargando PDF: {e}")
        return False

def extraer_texto_ocr(ruta_pdf):
    """
    Convierte PDF a imágenes y aplica OCR. 
    Maneja documentos escaneados optimizando la imagen antes de leer.
    """
    print("👀 Iniciando proceso de OCR (esto puede tardar un poco)...")
    texto_consolidado = ""
    
    try:
        # 1. Convertir PDF a lista de imágenes (Pillow Objects)
        # dpi=300 es el estándar para buen OCR.
        imagenes = convert_from_path(ruta_pdf, dpi=300, poppler_path=POPPLER_PATH)
        
        total_paginas = len(imagenes)
        print(f"📄 Documento tiene {total_paginas} páginas.")

        for i, imagen in enumerate(imagenes):
            print(f"   - Procesando página {i+1}/{total_paginas}...")
            
            # Opcional: Aquí podrías usar Pillow para aumentar contraste si el scan es muy malo
            # imagen = imagen.convert('L') # Escala de grises
            
            # 2. Aplicar Tesseract
            # lang='spa' es vital si el documento está en español
            texto_pagina = pytesseract.image_to_string(imagen, lang='spa')
            
            texto_consolidado += f"\n--- PÁGINA {i+1} ---\n"
            texto_consolidado += texto_pagina
            
        print("✅ OCR Finalizado.")
        return texto_consolidado

    except Exception as e:
        print(f"❌ Error crítico en OCR: {e}")
        return None

def limpiar_y_estructurar_con_gemini(texto_crudo_ocr, datos_mineduc_extra=None):
    """
    Envía el texto sucio a Gemini y solicita un JSON limpio.
    """
    print("🤖 Enviando datos a Gemini para limpieza y estructuración...")
    
    # Configuración del modelo (usamos el modelo Pro para mejor razonamiento o Flash para velocidad)
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    # Prompt Engineering: Contexto + Tarea + Formato de Salida
    prompt = f"""
    Actúa como un analista de datos experto. Tengo un texto extraído vía OCR de un documento escaneado (PDF de la UCM) y puede contener errores tipográficos, caracteres extraños o saltos de línea incorrectos.

    TAREA:
    1. Analiza el siguiente TEXTO CRUDO.
    2. Identifica los campos clave relevantes para postulantes a beneficios estudiantiles (fechas, requisitos, montos, sedes, nombres de becas).
    3. Corrige la ortografía y gramática de los valores extraídos.
    4. Estructura la salida ESTRICTAMENTE en formato JSON.

    TEXTO CRUDO:
    {texto_crudo_ocr}

    FORMATO DE RESPUESTA ESPERADO (Solo JSON, sin bloques de código markdown):
    {{
        "institucion": "Universidad Católica del Maule",
        "documento_origen": "Nombre detectado o inferido",
        "beneficios_detectados": [
            {{
                "nombre": "...",
                "descripcion": "...",
                "requisitos": ["..."],
                "fechas_clave": "..."
            }}
        ],
        "observaciones": "Resumen breve del contenido"
    }}
    """

    try:
        response = model.generate_content(prompt)
        texto_respuesta = response.text
        
        # Limpieza simple por si el modelo devuelve ```json ... ```
        texto_limpio = texto_respuesta.replace("```json", "").replace("```", "").strip()
        
        datos_json = json.loads(texto_limpio)
        print("✨ Datos estructurados exitosamente.")
        return datos_json

    except json.JSONDecodeError:
        print("⚠️ El modelo no devolvió un JSON válido. Se devuelve texto plano.")
        return {"error": "JSON invalido", "raw_response": response.text}
    except Exception as e:
        print(f"❌ Error en la API de Gemini: {e}")
        return None

# ==========================================
# 3. BLOQUE PRINCIPAL DE EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    # URL de ejemplo (esto vendría de tu scrapeo con Selenium)
    URL_PDF_UCM = "https://portal.ucm.cl/content/uploads/2016/12/Decreto_de_Rectoria_141-2022.pdf" 
    RUTA_LOCAL_PDF = 'C:\Decreto_de_Rectoria_141-2022.pdf'
    
    # 1. Descargar (o usar Selenium si la descarga requiere interacción compleja)
    # Si ya tienes el PDF descargado, puedes comentar esta línea.
    # descargar_pdf_con_requests(URL_PDF_UCM, RUTA_LOCAL_PDF)
    
    # Asegúrate de que el archivo exista antes de procesar
    if os.path.exists(RUTA_LOCAL_PDF):
        
        # 2. OCR
        texto_sucio = extraer_texto_ocr(RUTA_LOCAL_PDF)
        
        if texto_sucio:
            # Simulamos datos que vendrían de tu scraping al MINEDUC
            datos_mineduc = "El MINEDUC informa que el proceso de gratuidad inicia el 1 de Octubre."
            
            # 3. IA - Limpieza y Estructura
            resultado_json = limpiar_y_estructurar_con_gemini(texto_sucio, datos_mineduc)
            
            # Guardar resultado
            with open("datos_finales.json", "w", encoding="utf-8") as f:
                json.dump(resultado_json, f, indent=4, ensure_ascii=False)
                print("💾 Archivo 'datos_finales.json' guardado.")
    else:
        print(f"No se encontró el archivo {RUTA_LOCAL_PDF}. Verifica la descarga.")