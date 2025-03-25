from dotenv import load_dotenv
import os 
from flask import Flask, render_template, request, session
import pandas as pd
import joblib
from pymongo import MongoClient
from flask_session import Session

app = Flask(__name__)

# Session-Konfiguration
app.config['SECRET_KEY'] = 'geheimerschluessel123'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Modell laden
model = joblib.load('models/car_price_predictor.joblib')

# MongoDB verbinden für Markenliste
MONGODB_URI = os.getenv('MONGODB_URI')
DATABASE = 'carpredictor'
COLLECTION = 'cars'

client = MongoClient(MONGODB_URI)
db = client[DATABASE]
collection = db[COLLECTION]


def get_brands():
    return sorted(collection.distinct('brand'))


@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    brands = get_brands()

    # Vorherige Einträge laden oder initialisieren
    if 'entries' not in session:
        session['entries'] = []

    if request.method == 'POST':
        brand = request.form['brand']
        model_year = int(request.form['model_year'])
        kilometer = int(request.form['kilometer'])
        fuel_type = request.form['fuel_type']
        accident = request.form['accident']

        input_df = pd.DataFrame({
            'brand': [brand],
            'model_year': [model_year],
            'kilometer': [kilometer],
            'fuel_type': [fuel_type],
            'accident': [accident]
        })

        training_columns = model.feature_names_in_
        input_encoded = pd.get_dummies(input_df).reindex(
            columns=training_columns, fill_value=0)

        prediction = round(model.predict(input_encoded)[0], 2)

        # Eingaben speichern und max. 5 Einträge behalten
        entry = {
            'brand': brand,
            'model_year': model_year,
            'kilometer': kilometer,
            'fuel_type': fuel_type,
            'accident': accident,
            'prediction': prediction
        }
        session['entries'].insert(0, entry)  # Neueste oben
        session['entries'] = session['entries'][:5]
        session.modified = True  # Session speichern

    return render_template('index.html', prediction=prediction, brands=brands, entries=session['entries'])


if __name__ == '__main__':
    app.run(debug=True)
