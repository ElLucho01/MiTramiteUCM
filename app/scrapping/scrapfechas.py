import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import google.generativeai as genai

# Configuración de la API de Gemini
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Por favor configura la variable de entorno GEMINI_API_KEY o inserta tu clave en el código.")

genai.configure(api_key=api_key)

def obtener_fechas_selenium():
    # Configuración de Chrome (Headless para que no abra la ventana visualmente)
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Inicializar el driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    datos_crudos = []

    try:
        print("1. Accediendo al sitio web...")
        url = "https://postulacion.beneficiosestudiantiles.cl/fuas/"
        driver.get(url)

        # Esperar un momento a que cargue el contenido (simple wait)
        time.sleep(2) 

        print("2. Rescatando datos del elemento...")
        # El XPath proporcionado por el usuario
        xpath_selector = "/html/body/main/section[1]/div/div/div/div/ul"
        
        contenedor_ul = driver.find_element(By.XPATH, xpath_selector)
        
        # Obtenemos los elementos de la lista (li) dentro del ul
        items = contenedor_ul.find_elements(By.TAG_NAME, "li")
        
        for item in items:
            text = item.text.strip()
            if text:
                datos_crudos.append(text)
        
        print(f"   -> Se encontraron {len(datos_crudos)} elementos.")

    except Exception as e:
        print(f"Error durante el scraping: {e}")
    finally:
        driver.quit()
    
    return datos_crudos

def procesar_con_gemini(lista_textos):
    print("3. Procesando datos con Gemini para formato JSON...")
    
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    prompt = f"""
    Actúa como un parser de datos. Tengo una lista de textos extraídos de un sitio web de becas estudiantiles.
    Tu tarea es convertir esta lista en un objeto JSON estructurado.
    
    Reglas:
    1. Si el texto indica un rango (ej: "del 1 de octubre al 22 de octubre"), extrae "fecha_inicio" y "fecha_termino".
    2. Si el texto es una fecha única (ej: "17 de diciembre 2025"), usa "fecha_publicacion".
    3. Normaliza las fechas al formato YYYY-MM-DD si es posible inferir el año, si no, mantenlo legible.
    4. La clave (key) debe ser el nombre del evento (ej: "Fecha de postulación").
    5. Responde SOLAMENTE con el JSON válido, sin bloques de código markdown ```json ... ``` ni explicaciones extra.

    Lista de entrada:
    {lista_textos}
    """

    try:
        response = model.generate_content(prompt)
        # Limpieza por si el modelo incluye backticks
        json_str = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(json_str)
    except Exception as e:
        print(f"Error procesando con IA: {e}")
        return {"error": "No se pudo procesar el JSON", "raw_data": lista_textos}

# --- Ejecución Principal ---
if __name__ == "__main__":
    # Paso 1 y 2: Scraping
    textos_extraidos = obtener_fechas_selenium()
    
    if textos_extraidos:
        # Paso 3: Formateo con IA
        resultado_json = procesar_con_gemini(textos_extraidos)
        
        # --- NUEVO CÓDIGO PARA GUARDAR EL ARCHIVO ---
        nombre_archivo = "resultados_fuas.json"
        
        # Abrimos (o creamos) el archivo en modo escritura ('w') con encoding utf-8
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            json.dump(resultado_json, archivo, indent=4, ensure_ascii=False)
            
        print(f"✅ ¡Listo! El archivo se ha guardado como '{nombre_archivo}' en la misma carpeta de este script.")
        
        # Opcional: Seguir imprimiendo en pantalla para verificar
        print(json.dumps(resultado_json, indent=4, ensure_ascii=False))