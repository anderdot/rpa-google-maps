import logging
from config import LOG_LEVEL

def configurar_logger(caminho_log):
    """
    Configura o logger para gravar mensagens em um arquivo e no console.

    Args:
        caminho_log (str): Caminho do arquivo de log a ser criado.
    """
    logger = logging.getLogger()
    # Define o nível de log com base na configuração fornecida em config.py
    logger.setLevel(LOG_LEVEL)

    if logger.handlers:
        return

    # Formato do log com data, nível, nome do logger e mensagem
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    # Configuração do handler para arquivo de log
    file_handler = logging.FileHandler(caminho_log, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Configuração do handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Ajusta o nível de log para bibliotecas externas para WARNING
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
