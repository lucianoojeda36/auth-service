#!/bin/bash

# Activar el entorno virtual
source ./venv/bin/activate

# Cargar las variables de entorno
export $(grep -v '^#' ./.env | xargs)

# Iniciar el servidor Django
exec python manage.py runserver $HOST:$PORT
