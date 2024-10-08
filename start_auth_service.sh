#!/bin/bash

# Activar el entorno virtual
source /home/ec2-user/myenv/bin/activate

# Cargar las variables de entorno
export $(grep -v '^#' ./.env | xargs)

# Imprimir las variables de entorno para verificar
echo "HOST: $HOST"
echo "PORT: $PORT"

# Iniciar el servidor Django
exec python3 manage.py runserver $HOST:$SERVICE_PORT