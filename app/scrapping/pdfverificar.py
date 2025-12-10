import requests

url_pdf = "https://www.ucm.cl/url-del-decreto/Decreto_de_Rectoria_141-2022.pdf" # Tu enlace real

# Estos encabezados engañan al servidor
headers = {
    # Simula ser un navegador Chrome en Windows
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    
    # ¡CRUCIAL! Le dice al servidor que vienes de su propia página web
    'Referer': 'https://www.ucm.cl/', 
    
    # Opcional pero recomendado:
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8'
}

# 2. Realizar la petición usando una Sesión
# Usar 'Session' maneja las cookies automáticamente si hay redirecciones intermedias
session = requests.Session()

try:
    response = session.get(url_pdf, headers=headers, timeout=10)
    
    # Verificar si fuimos redirigidos (código 302/301) o si obtuvimos el PDF (200)
    if response.status_code == 200 and 'application/pdf' in response.headers.get('Content-Type', ''):
        with open("Decreto_141-2022.pdf", "wb") as f:
            f.write(response.content)
        print("¡PDF descargado con éxito!")
    else:
        print(f"Error: El servidor devolvió código {response.status_code}")
        print(f"Tipo de contenido recibido: {response.headers.get('Content-Type')}")
        # Si sigue redirigiendo a ucm.cl, imprimirá text/html en lugar de pdf
        
except Exception as e:
    print(f"Ocurrió un error en la conexión: {e}")