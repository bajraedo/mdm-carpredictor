import os
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile


def download_and_extract():
    api = KaggleApi()
    api.authenticate()

    dataset_owner_slug = "taeefnajib/used-car-price-prediction-dataset"
    download_path = "./data"

    print("Starte Download von Kaggle...")
    api.dataset_download_files(
        dataset_owner_slug, path=download_path, unzip=False, quiet=False)

    zip_file_path = os.path.join(
        download_path, "used-car-price-prediction-dataset.zip")

    if os.path.exists(zip_file_path):
        print(f"Zip-Datei gefunden: {zip_file_path}")
        print("Inhalt der ZIP-Datei:")
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.printdir()
            zip_ref.extractall(download_path)
        os.remove(zip_file_path)
        print("Zip-Datei erfolgreich extrahiert und entfernt!")
    else:
        print("Keine ZIP-Datei gefunden. Prüfe den Pfad und API-Key.")


if __name__ == "__main__":
    download_and_extract()
