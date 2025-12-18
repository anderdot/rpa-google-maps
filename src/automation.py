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

# Configuração do logger para este módulo
log = logging.getLogger(__name__)

def validar_raio():
    """
    Valida o valor do raio utilizado na requisição da API do Google Maps.

    A API do Google Maps exige que o raio esteja dentro do intervalo
    permitido de 1 a 50.000 metros. Caso o valor configurado esteja
    fora desse intervalo, a função interrompe o fluxo lançando uma
    exceção.

    Raises:
        ValueError: Se o valor do raio for menor ou igual a zero
        ou maior que 50.000 metros.
    """
    if RAIO <= 0 or RAIO > 50000:
        raise ValueError(
            f"Raio inválido: {RAIO}. Deve estar entre 1 e 50000 metros."
        )


def criar_params(tipo_api, pagetoken=None):
    """
    Cria os parâmetros para a requisição à API do Google Maps.

    Args:
        tipo_api (str): Tipo do estabelecimento a ser pesquisado.
        pagetoken (str, optional): Token para paginação dos resultados. Defaults to None.

    Returns:
        dict: Dicionário contendo os parâmetros para a requisição à API.
    """
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
    """
    Realiza a requisição à API do Google Maps com os parâmetros fornecidos.

    Args:
        params (dict): Dicionário contendo os parâmetros para a requisição à API.

    Returns:
        dict: Dicionário contendo os dados da resposta da API.
    """
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
    """
    Valida a resposta da API do Google Maps.

    Args:
        dados (dict): Dicionário contendo os dados da resposta da API.

    Raises:
        RuntimeError: Se o status da resposta for "OK" ou "ZERO_RESULTS".
    """
    status = dados.get("status")

    if status in ("OK", "ZERO_RESULTS"):
        return

    mensagem = dados.get("error_message", "Sem mensagem de erro")
    raise RuntimeError(f"Erro da API Google: {status} - {mensagem}")


def paginar_resultados(tipo_api, tipo_legivel):
    """
    Realiza a paginação dos resultados da API do Google Maps.

    A API do Google Maps retorna um número limitado de resultados por
    requisição. Esta função gerencia a paginação, coletando todos os
    resultados disponíveis. O máximo de resultados retornados pela API
    é de 60 registros (20 por página).

    Args:
        tipo_api (str): Tipo do estabelecimento a ser pesquisado.
        tipo_legivel (str): Tipo legível do estabelecimento a ser pesquisado.

    Returns:
        tuple: Tupla contendo os dados coletados e o total de registros.
    """
    dados = []
    total = 0
    pagina = 1
    pagetoken = None

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

        # Aguarda alguns segundos antes de fazer a próxima requisição (como exigido pela API)
        time.sleep(2)
        pagina += 1

    log.info(f"{tipo_legivel}: {total} registros coletados.")
    return dados, total


def coletar_dados(caminhos_arquivos):
    """
    Coleta os dados da API do Google Maps e exporta para arquivos.

    Args:
        caminhos_arquivos (dict): Dicionário contendo os caminhos dos arquivos de exportação.
    """
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
