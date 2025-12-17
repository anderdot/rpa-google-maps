import json
from config import (
    LATITUDE,
    LONGITUDE,
    RAIO,
    DATA_DIR,
    TIMESTAMP
)

def normalizar_dados(dados, tipo_localizado):
    dados_normalizados = []
    for item in dados:
        nome_estabelecimento = item.get("name", "N/A")
        tipo = tipo_localizado
        nota_estabelecimento = item.get("rating", "N/A")
        quantidade_avaliacoes = item.get("user_ratings_total", "N/A")
        endereco_completo = item.get("vicinity", "N/A")

        dados_normalizados.append({
            "nome_estabelecimento": nome_estabelecimento,
            "tipo": tipo,
            "nota_estabelecimento": nota_estabelecimento,
            "quantidade_avaliacoes": quantidade_avaliacoes,
            "endereco_completo": endereco_completo
        })
    return dados_normalizados

def criar_nome_arquivo(extensao):
    lat = str(LATITUDE).replace(".", "-")
    lon = str(LONGITUDE).replace(".", "-")
    rai = str(RAIO)
    nome_arquivo = f"estabelecimentos_lat{lat}_lon{lon}_rai_{rai}_{TIMESTAMP}.{extensao}"

    return nome_arquivo

def gerar_json(dados):
    nome_arquivo = criar_nome_arquivo("json")
    with open(DATA_DIR / nome_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=2, ensure_ascii=False)
