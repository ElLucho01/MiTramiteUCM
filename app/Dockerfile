# Imagen base
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar los archivos de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Instalar netcat para poder esperar a la DB
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

# Copiar todo el proyecto al contenedor
COPY . .

# Copiar y asignar permisos al script de espera
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exponer el puerto de Flask (por defecto 5000)
EXPOSE 5000

# Usar el entrypoint
ENTRYPOINT ["/entrypoint.sh"]

