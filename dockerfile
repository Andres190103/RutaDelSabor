# 1. IMAGEN BASE
# Usamos una versión ligera de Linux que ya tiene Python 3.9 instalado.
# Es como decir: "Dame una compu vacía con Python".
FROM python:3.9-slim

# 2. OPTIMIZACIONES DE PYTHON
# PYTHONDONTWRITEBYTECODE: Evita que Python cree archivos .pyc (basura en docker)
# PYTHONUNBUFFERED: Hace que los logs (print) salgan directo a la consola sin retraso
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. DIRECTORIO DE TRABAJO
# Creamos una carpeta llamada /app dentro del contenedor y nos metemos ahí.
WORKDIR /app

# 4. INSTALACIÓN DE DEPENDENCIAS DEL SISTEMA
# PostgreSQL necesita librerías de C (gcc, libpq-dev) para poder instalarse.
# Esto es equivalente a usar apt-get install en Ubuntu.
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean

# 5. INSTALACIÓN DE LIBRERÍAS PYTHON
# Copiamos solo el requirements.txt primero (para aprovechar la caché de Docker)
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Instalamos librerías extra necesarias para Producción/Docker que quizás no tenías
RUN pip install gunicorn psycopg2-binary dj-database-url

# 6. COPIAR EL CÓDIGO
# Copiamos todo tu proyecto (.) a la carpeta de trabajo del contenedor (/app/)
COPY . /app/

# 7. COMANDO DE ARRANQUE
# Cuando el contenedor inicie, ejecutará este comando.
# 0.0.0.0:8000 permite recibir conexiones desde fuera del contenedor.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]