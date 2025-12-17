import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega a chave da API do arquivo .env
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Configurações do Google Maps API
GOOGLE_MAPS_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
LATITUDE = -23.5505
LONGITUDE = -46.633306
RAIO = 1000

# Mapeamento dos tipos do Google Maps para nomes em português
# https://developers.google.com/maps/documentation/places/web-service/place-types?hl=pt-br
TIPOS = {
    "gym": "academia",
    "restaurant": "restaurante",
    "ice_cream_shop": "sorveteria"
}

# Criação de diretórios
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = BASE_DIR / "exports"

DATA_DIR.mkdir(exist_ok=True)
EXPORTS_DIR.mkdir(exist_ok=True)
