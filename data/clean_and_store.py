import pandas as pd
from pymongo import MongoClient

MONGODB_URI = 'mongodb+srv://carpredictor_user:Prima25vera@cluster0.sb2y7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
DATABASE = 'carpredictor'
COLLECTION = 'cars'

df = pd.read_csv('data/used_cars.csv')

print(f"Original-Datensatz enthält {len(df)} Zeilen.")

df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

print(f"Nach Entfernen von Duplikaten und fehlenden Werten: {len(df)} Zeilen.")

# Relevante Spalten auswählen und umbenennen
df = df[['brand', 'model_year', 'milage', 'fuel_type', 'accident', 'price']]
df.rename(columns={'milage': 'kilometer'}, inplace=True)

# Kilometer bereinigen
df['kilometer'] = df['kilometer'].str.replace(',', '', regex=False)
df['kilometer'] = df['kilometer'].str.replace(
    'mi.', '', regex=False).str.strip()
df['kilometer'] = pd.to_numeric(df['kilometer'], errors='coerce')
df.dropna(subset=['kilometer'], inplace=True)

print(f"Nach Bereinigung Kilometer: {len(df)} Zeilen.")

# Umrechnung Meilen zu Kilometer
df['kilometer'] = (df['kilometer'] * 1.60934).round(0).astype(int)

# Treibstoffarten anpassen
df['fuel_type'] = df['fuel_type'].map({
    'Gasoline': 'Benzin',
    'Diesel': 'Diesel',
    'Electric': 'Elektrisch',
    'Hybrid': 'Hybrid'
})
df.dropna(subset=['fuel_type'], inplace=True)

print(f"Nach Bereinigung fuel_type: {len(df)} Zeilen.")

# Preis bereinigen ($ und Kommas entfernen)
df['price'] = df['price'].str.replace('$', '', regex=False)
df['price'] = df['price'].str.replace(',', '', regex=False)
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df.dropna(subset=['price'], inplace=True)

print(f"Nach Bereinigung Preis: {len(df)} Zeilen.")

# Preis von USD nach CHF umrechnen
df['price'] = (df['price'] * 0.92).round(2)

# Finale Datentypen setzen
df['model_year'] = df['model_year'].astype(int)
df['accident'] = df['accident'].astype(str)

# Prüfung, ob Daten verbleiben
if df.empty:
    print("DataFrame ist leer! Keine Daten zum Speichern.")
else:
    print(f"Endgültige Anzahl Datensätze zum Speichern: {len(df)}")
    client = MongoClient(MONGODB_URI)
    db = client[DATABASE]
    collection = db[COLLECTION]
    collection.insert_many(df.to_dict(orient='records'))
    print("Daten erfolgreich gespeichert.")
