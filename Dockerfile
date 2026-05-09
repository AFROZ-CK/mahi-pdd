# DataMind container image
FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt /app/app/requirements.txt
RUN pip install --no-cache-dir -r /app/app/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["python", "app/main.py"]
