#!/bin/sh

echo "⏳ Esperando a que la base de datos PostgreSQL esté lista..."

# Esperar a que el contenedor 'db' responda en el puerto 5432
while ! nc -z db 5432; do
  sleep 1
done

echo "✅ Base de datos disponible, iniciando Flask..."
exec python app.py