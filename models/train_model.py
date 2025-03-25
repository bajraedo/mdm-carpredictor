import pandas as pd
from pymongo import MongoClient
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Verbindung zu MongoDB
MONGODB_URI = 'mongodb+srv://carpredictor_user:Prima25vera@cluster0.sb2y7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
DATABASE = 'carpredictor'
COLLECTION = 'cars'

client = MongoClient(MONGODB_URI)
db = client[DATABASE]
collection = db[COLLECTION]

# Daten laden und in DataFrame umwandeln
df = pd.DataFrame(list(collection.find()))

# MongoDB-interne ID-Spalte entfernen
if '_id' in df.columns:
    df.drop(columns=['_id'], inplace=True)

print(f"Geladene Daten aus MongoDB: {len(df)} Zeilen")

# Features und Zielvariable definieren
X = df[['brand', 'model_year', 'kilometer', 'fuel_type', 'accident']]
y = df['price']

# Kategorische Variablen (brand, fuel_type, accident) one-hot-encoden
X_encoded = pd.get_dummies(
    X, columns=['brand', 'fuel_type', 'accident'], drop_first=True)

# Daten in Trainings- und Testset aufteilen
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42)

print(f"Training-Daten: {X_train.shape}, Test-Daten: {X_test.shape}")

# Modelltraining und Hyperparameter-Optimierung mit GridSearchCV
rf = RandomForestRegressor(random_state=42)

# Parameter für GridSearchCV
param_grid = {
    'n_estimators': [50, 100, 150],
    'max_depth': [5, 10, 20],
    'min_samples_split': [2, 5, 10]
}

print("Starte GridSearchCV (dies könnte einige Minuten dauern)...")
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid,
                           cv=5, n_jobs=-1, scoring='neg_mean_squared_error')

grid_search.fit(X_train, y_train)

# Ausgabe der besten Parameter
print("Beste Hyperparameter gefunden:")
print(grid_search.best_params_)

# Bestes Modell verwenden
best_model = grid_search.best_estimator_

# Vorhersage auf Testdaten
y_pred = best_model.predict(X_test)

# Modell evaluieren
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Modell-Performance auf Testdaten:")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"R² Score: {r2:.2f}")

# Trainiertes Modell speichern
joblib.dump(best_model, 'models/car_price_predictor.joblib')
print("Trainiertes Modell erfolgreich gespeichert unter 'models/car_price_predictor.joblib'")
