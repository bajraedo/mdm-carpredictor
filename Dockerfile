# Basis-Image mit Python 3.11
FROM python:3.11-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Projektdateien (inkl. .env) kopieren
COPY . .

# Port für Gunicorn/Flask freigeben
EXPOSE 5000

# Startbefehl mit Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.app:app"]
