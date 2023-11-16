FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080

EXPOSE $PORT

# Utiliza el comando de ejecución con la expansión de la variable de entorno
CMD ["uvicorn", "router.main:app", "--host", "0.0.0.0", "--port", "${PORT}"]
