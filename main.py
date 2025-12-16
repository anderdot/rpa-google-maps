import requests
import dotenv
import json

dotenv.load_dotenv()
api_key = dotenv.get_key(".env", "GOOGLE_API_KEY")
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
latitude = -23.5505
longitude = -46.633306
raio = 1000
tipo_google = "restaurant"

params = {
    "key": api_key,
    "location": f"{latitude},{longitude}",
    "radius": raio,
    "type": tipo_google,
    "language": "pt-BR"
}

resultados = []
while True:
    resposta = requests.get(url, params=params).json()

    for lugar in resposta.get("results", []):
        resultados.append({
            "nome": lugar.get("name"),
            "tipo": tipo_google,
            "nota": lugar.get("rating"),
            "quantidade_avaliacoes": lugar.get("user_ratings_total"),
            "endereco_completo": lugar.get("vicinity")
        })

    if "next_page_token" not in resposta:
        break

    params["pagetoken"] = resposta["next_page_token"]

print(json.dumps(resultados, ensure_ascii=False, indent=2))
