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

def validar_raio():
    if RAIO <= 0 or RAIO > 50000:
        raise ValueError(
            f"Raio inválido: {RAIO}. Deve estar entre 1 e 50000 metros."
        )

def criar_params(tipo_api, pagetoken=None):
    params = {
        "key": API_KEY,
        "location": f"{LATITUDE},{LONGITUDE}",
        "radius": RAIO,
        "type": tipo_api,
        "language": "pt-BR"
    }

    if pagetoken:
        params["pagetoken"] = pagetoken

    return params

def requisitar_api(params):
    try:
        log.debug(f"Requisitando API com params: {params}.")

        resposta = requests.get(
            GOOGLE_MAPS_URL,
            params=params,
            timeout=10
        )

        resposta.raise_for_status()
        return resposta.json()

    except requests.exceptions.RequestException as erro:
        log.error(f"Erro na requisição HTTP: {erro}.")
        raise

def validar_resposta_api(dados):
    status = dados.get("status")

    if status in ("OK", "ZERO_RESULTS"):
        return

    mensagem = dados.get("error_message", "Sem mensagem de erro")
    raise RuntimeError(f"Erro da API Google: {status} - {mensagem}")

def paginar_resultados(tipo_api, tipo_legivel):
    dados = []
    total = 0
    pagetoken = None
    pagina = 1

    while True:
        log.debug(f"Página {pagina} - Tipo {tipo_legivel}")

        params = criar_params(tipo_api, pagetoken)
        resposta = requisitar_api(params)
        validar_resposta_api(resposta)

        resultados = resposta.get("results", [])
        total += len(resultados)

        dados.extend(normalizar_dados(resultados, tipo_legivel))

        pagetoken = resposta.get("next_page_token")
        if not pagetoken:
            break

        time.sleep(2)
        pagina += 1

    log.info(f"{tipo_legivel}: {total} registros coletados.")
    return dados, total

def coletar_dados(caminhos_arquivos):
    try:
        validar_raio()
    except ValueError as erro:
        log.critical(str(erro))
        return

    log.info("Iniciando coleta de dados.")
    dados = []
    total_geral = 0

    for tipo_api, tipo_legivel in TIPOS.items():
        try:
            dados_tipo, total_tipo = paginar_resultados(
                tipo_api,
                tipo_legivel
            )
            dados.extend(dados_tipo)
            total_geral += total_tipo

        except Exception as erro:
            log.error(
                f"Erro ao coletar dados de {tipo_legivel}: {erro}.",
                exc_info=True
            )

    log.info(f"Coleta finalizada. Total geral: {total_geral}.")

    log.info("Exportando dados.")
    exportar_dados(dados, caminhos_arquivos)
    log.info("Exportação concluída com sucesso.")
