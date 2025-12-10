import os
import time
import json
import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 1. Configuración de Gemini AI
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Error: No se encontró la variable de entorno 'GEMINI_API_KEY'")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite') # Modelo rápido y eficiente para texto

def procesar_con_gemini(html_table):
    """
    Envía el HTML de la tabla a Gemini para que lo convierta en un JSON estructurado
    separando el número de la causal y su nombre descriptivo.
    """
    prompt = f"""
    Actúa como un experto en extracción de datos y estructuración de información legal/administrativa.
    Tengo el siguiente código HTML de una tabla extraída de una web (referente a Causales de Apelación).

    Tu tarea es generar un JSON válido siguiendo estas reglas estrictas:

    1. ANÁLISIS DE COLUMNAS:
       - La **Columna 1** contiene la 'Causal'. Esta celda incluye un NÚMERO y un NOMBRE (Texto descriptivo). DEBES separarlos. 
         (Ejemplo visual: "1 Diferencias..." -> numero: "1", nombre: "Diferencias...").
       - La **Columna 2** contiene 'Documentación' o 'Trámites'. Esta celda suele tener múltiples requisitos (puntos, items).

    2. REGLA DE EXPANSIÓN (FLATTENING):
       - La segunda columna contiene múltiples documentos/trámites en una misma celda. DEBES separar cada uno de estos ítems individualmente.
       - Si la celda 2 lista 3 documentos distintos, debes generar 3 objetos JSON separados.
       - En cada objeto, repite los datos de la Columna 1 (numero y nombre) asociados a ese documento específico.

    3. ESTRUCTURA DE SALIDA:
       Genera una lista plana de objetos donde cada objeto tenga exactamente esta estructura:
       {{
           "numero": "El número extraído de la columna 1",
           "nombre": "El texto descriptivo de la etapa/causal extraído de la columna 1 (sin el número)",
           "documento": "El texto del trámite o documento individual extraído de la columna 2"
       }}

    4. LIMPIEZA:
       - Elimina viñetas, puntos extra al inicio o final, y textos como "(Obligatorio)" si no aportan al nombre del documento, o déjalo si es relevante según el contexto.
       - Responde SOLAMENTE con el JSON crudo, sin bloques de código markdown (```json).

    HTML DE LA TABLA:
    {html_table}
    """
    
    # Aquí iría tu llamada a la API (ej: model.generate_content(prompt))
    # return response.text
    
    try:
        response = model.generate_content(prompt)
        # Limpieza por si Gemini incluye markdown
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except Exception as e:
        print(f"Error al procesar con IA: {e}")
        return None

# 2. Configuración de Selenium
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--ignore-certificate-errors") # Ayuda con algunos errores de SSL
options.add_argument("--no-sandbox")
options.add_argument("--headless") # Descomenta esto si no quieres ver el navegador abrirse

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20) # Espera explícita de hasta 20 segundos

try:
    print("--- Paso 1: Entrando a la página ---")
    url_objetivo = "https://portal.beneficiosestudiantiles.cl/guia-paso-paso-postulacion"
    driver.get(url_objetivo.strip())
    print("--- Paso 2: Haciendo click en la pestaña (Li 7) ---")
    # XPath proporcionado: /html/body/div[10]/section/div/div/ul/li[7]/a
    xpath_tab = "/html/body/div[10]/section/div/div/ul/li[7]/a"
    tab_element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_tab)))
    tab_element.click()
    
    # Pequeña pausa para asegurar que la animación del tab termine
    time.sleep(2)

    print("--- Paso 3: Haciendo click en el acordeón ---")
    # XPath proporcionado para el click
    xpath_accordion = "/html/body/div[10]/section/div/div/div/fieldset[7]/div/article/div/div[2]/div/div/div/div/div/div/div/div[1]"
    accordion_element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_accordion)))
    # A veces es necesario usar JavaScript click si el elemento está cubierto o es complejo
    driver.execute_script("arguments[0].click();", accordion_element)
    
    time.sleep(2) # Esperar despliegue del acordeón

    print("--- Paso 4: Rescatando información de la tabla ---")
    # XPath proporcionado para la tabla
    xpath_table = "/html/body/div[10]/section/div/div/div/fieldset[7]/div/article/div/div[2]/div/div/div/div/div/div/div/div[2]/div/div/table"
    table_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath_table)))
    
    # Obtenemos el HTML completo de la tabla para pasárselo a la IA
    table_html = table_element.get_attribute('outerHTML')
    print("Tabla extraída correctamente.")

    print("--- Paso 5: Generando JSON con Gemini ---")
    data_json = procesar_con_gemini(table_html)

    if data_json:
        # Guardar en archivo
        with open('resultado_tramites.json', 'w', encoding='utf-8') as f:
            json.dump(data_json, f, ensure_ascii=False, indent=4)
        
        print("\n¡Éxito! El JSON ha sido generado:")
        print(json.dumps(data_json, ensure_ascii=False, indent=2))
    else:
        print("No se pudo generar el JSON.")

except Exception as e:
    print(f"Ocurrió un error durante la ejecución: {e}")

finally:
    driver.quit()