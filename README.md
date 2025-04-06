# Car Price Predictor – Gebrauchtwagen Preisprognose

End-to-End Lösung zur Vorhersage von Gebrauchtwagenpreisen auf Basis öffentlich verfügbarer Daten von Kaggle – umgesetzt als Web-App mit Azure Deployment und Docker.

---

## Datenquelle

- **Datensatz:** [Used Car Price Prediction Dataset](https://www.kaggle.com/datasets/taeefnajib/used-car-price-prediction-dataset)
- **Abruf:** über die Kaggle API
- Speicherung der Rohdaten als `.csv`
- Bereinigung und Transformation mit `pandas`
- Speicherung der bereinigten Daten in **MongoDB Atlas**

---

## Datenaufbereitung

- Umrechnung von Meilen in Kilometer  
- Umrechnung von USD in CHF  
- Vereinheitlichung der Treibstoffarten auf Schweizer Standards  
  *(Benzin, Diesel, Elektrisch, Hybrid)*
- Auswahl relevanter Features:  
  `brand`, `model_year`, `kilometer`, `fuel_type`, `accident`, `price`

---

## Model Training

**Vorverarbeitung:**

- Feature Engineering  
- One-Hot-Encoding

**Verglichene Modelle:**

- Lineare Regression  
- Random Forest  
- Gradient Boosting

**Evaluationsmetriken:**

- MSE  
- R²  

**Bestes Modell:**  
Random Forest Regressor mit einem R² Score von **0.59**  
Gespeichert als `.joblib`-Datei

---

## Azure Blob Storage

- Automatischer Upload des trainierten Modells in **Azure Blob Storage**
- Container: `models`
- Zugriff über die Umgebungsvariable `AZURE_STORAGE_CONNECTION_STRING`
- Bereit für zukünftige CI/CD-Integrationen

---

## Docker & Deployment

- Dockerisierung mit `Dockerfile`
- Nutzung von `Gunicorn` als Produktionsserver
- Architektur: `linux/amd64` für Azure-Kompatibilität
- Push auf Docker Hub:  
  `bajraedo/carpredictor-app:latest`
- Deployment auf **Azure App Service for Containers**
- Live:  
  `https://mdm-backend-app.azurewebsites.net`

---

## Web-App

### Backend

- Python Flask (`app/app.py`)
- Lädt das Modell bei Start
- Holt dynamisch Markenliste aus MongoDB

### Frontend

- HTML/CSS mit Bootstrap  
- Responsives Design  
- Eingabefelder für:
  - Automarke
  - Baujahr
  - Kilometerstand
  - Treibstoff
  - Unfallstatus
- Ausgabe der Preisprognose direkt im UI
- Speicherung der letzten fünf Eingaben mit Flask-Session

---

## Sicherheit & Struktur

- `.env` für sensible Daten wie MongoDB URI
- `.gitignore` schützt sensible Dateien
- Projektstruktur:
