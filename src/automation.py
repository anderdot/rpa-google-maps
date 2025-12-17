import requests
import json
from src.utils import normalizar_dados
from config import (
    API_KEY,
    GOOGLE_MAPS_URL,
    LATITUDE,
    LONGITUDE,
    RAIO,
    TIPOS,
)

def requisitar_api(params):
    resposta = requests.get(GOOGLE_MAPS_URL, params=params)
    return resposta.json()

def coletar_dados():
    dados = []

    for tipo_api, tipo_localizado in TIPOS.items():
        params = {
            "key": API_KEY,
            "location": f"{LATITUDE},{LONGITUDE}",
            "radius": RAIO,
            "type": tipo_api,
            "language": "pt-BR"
        }

        resposta = requisitar_api(params)
        resposta_normalizada = normalizar_dados(resposta.get("results", []), tipo_localizado)
        dados.extend(resposta_normalizada)

    print(json.dumps(dados, indent=2, ensure_ascii=False))
