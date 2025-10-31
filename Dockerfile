# Imagen base de Python
FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar los archivos de requisitos e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código al contenedor
COPY . .

# Exponer el puerto donde correrá Flask
EXPOSE 5000

# Variable de entorno para Flask
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Comando para ejecutar Flask
CMD ["flask", "run"]
