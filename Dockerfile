# Usa la imagen oficial de Python como base
FROM python:3.9

# Evita que Python cree archivos .pyc y habilita la salida sin búfer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /usr/src/app

# Copia el archivo de requerimientos
COPY requirements.txt .

# Instala las dependencias
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean && \
    pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de la aplicación
COPY . .

# Ejecuta el comando collectstatic sin interacción si usas archivos estáticos
RUN python manage.py collectstatic --noinput

# Expone el puerto donde corre la aplicación Django
EXPOSE 8000

# Comando para ejecutar las migraciones y luego la aplicación Django
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
