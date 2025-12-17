import logging
import time
import requests
from src.utils.utils import normalizar_dados, exportar_dados
from config import (
    API_KEY,
    GOOGLE_MAPS_URL,
    LATITUDE,
    LONGITUDE,
    RAIO,
    TIPOS,
)

log = logging.getLogger(__name__)

def requisitar_api(params):
    log.debug(f"Requisitando dados da API com parâmetros: {params}")
    resposta = requests.get(GOOGLE_MAPS_URL, params=params, timeout=10)

    if resposta.status_code != 200:
        log.error(f"Erro na requisição: {resposta.status_code} - {resposta.text}.")
        return {}

    dados = resposta.json()

    if dados.get("status") not in ("OK", "ZERO_RESULTS"):
        log.error(f"Erro na resposta da API: {dados.get('status')} - {dados.get('error_message')}.")
        return {}

    log.debug(f"Resposta da API recebida com sucesso!")
    return dados

def coletar_dados(caminhos_arquivos):
    log.info("Iniciando coleta de dados")
    dados = []
    estabelecimentos_total = 0

    for tipo_api, tipo_localizado in TIPOS.items():
        log.info(f"Coletando dados para o tipo: {tipo_localizado}.")

        params = {
            "key": API_KEY,
            "location": f"{LATITUDE},{LONGITUDE}",
            "radius": RAIO,
            "type": tipo_api,
            "language": "pt-BR"
        }

        if RAIO <= 0 or RAIO > 50000:
            log.warning(f"Raio inválido: {RAIO}. Deve estar entre 1 e 50000 metros.")
            continue

        pagina = 1
        estabelecimentos_tipo = 0

        while True:
            log.debug(f"Requisitando página {pagina} para o tipo {tipo_localizado}.")

            resposta = requisitar_api(params)
            resultado = resposta.get("results", [])

            qtd_estabelecimento = len(resultado)
            estabelecimentos_tipo += qtd_estabelecimento

            if estabelecimentos_tipo == 0:
                log.warning(f"Nenhum registro encontrado para o tipo {tipo_localizado}.")
            else:
                log.debug(f"Recebidos {qtd_estabelecimento} estabelecimentos.")
                estabelecimentos_total += qtd_estabelecimento

            resposta_normalizada = normalizar_dados(resultado, tipo_localizado)
            dados.extend(resposta_normalizada)

            # Verifica se há uma próxima página de resultados
            if "next_page_token" not in resposta:
                log.debug(f"Todas as páginas coletadas para o tipo {tipo_localizado}.")
                break

            # Aguarda alguns segundos antes de fazer a próxima requisição (como exigido pela API)
            time.sleep(2)
            params["pagetoken"] = resposta["next_page_token"]
            pagina += 1

        log.info(f"Total de estabelecimentos coletados para o tipo {tipo_localizado}: {estabelecimentos_tipo}.")
    log.info(f"Coleta de dados concluída. Total de estabelecimentos coletados: {estabelecimentos_total}.")

    log.info("Exportando dados.")
    exportar_dados(dados, caminhos_arquivos)
    log.info("Dados exportados com sucesso.")
