import logging
from src.automation import coletar_dados
from src.utils.names import gerar_caminhos_arquivos
from src.utils.logger import configurar_logger

def main():
    caminhos_arquivos = gerar_caminhos_arquivos()

    try:
        configurar_logger(caminhos_arquivos["log"])
        log = logging.getLogger(__name__)
        log.info("Iniciando automação")

        coletar_dados(caminhos_arquivos)

        log.info("Automação concluída com sucesso")
    except Exception as erro:
        log.critical(f"Automação encerrada devido a um erro crítico: {erro}")

if __name__ == "__main__":
    main()
