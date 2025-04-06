from azure.storage.blob import BlobServiceClient
import os

# Verbindung zum Azure Blob Storage herstellen
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = 'models'
local_model_path = 'models/car_price_predictor.joblib'
blob_name = 'car_price_predictor.joblib'

# Blob-Service-Client erstellen
blob_service_client = BlobServiceClient.from_connection_string(
    connection_string)

# Blob-Client erzeugen
blob_client = blob_service_client.get_blob_client(
    container=container_name, blob=blob_name)

# Modell hochladen
with open(local_model_path, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print(
    f"Modell '{local_model_path}' erfolgreich hochgeladen nach '{container_name}/{blob_name}'")