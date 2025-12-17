import time
import requests
from src.utils import normalizar_dados, exportar_dados
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

        while True:
            resposta = requisitar_api(params)
            resultado = resposta.get("results", [])
            resposta_normalizada = normalizar_dados(resultado, tipo_localizado)
            dados.extend(resposta_normalizada)

            # Verifica se há uma próxima página de resultados
            if "next_page_token" not in resposta:
                break

            # Aguarda alguns segundos antes de fazer a próxima requisição (como exigido pela API)
            time.sleep(2)
            params["pagetoken"] = resposta["next_page_token"]

    exportar_dados(dados)
