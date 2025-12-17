from datetime import datetime
from config import (
    LATITUDE,
    LONGITUDE,
    RAIO,
    DATA_DIR,
    EXPORTS_DIR,
    LOGS_DIR
)

def gerar_caminhos_arquivos():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    lat = str(LATITUDE).replace(".", "-")
    lon = str(LONGITUDE).replace(".", "-")
    rai = str(RAIO)

    base = f"estabelecimentos_lat{lat}_lon{lon}_rai{rai}_{timestamp}"
    caminhos_arquivos = {
        "json": f"{DATA_DIR}/{base}.json",
        "excel": f"{EXPORTS_DIR}/{base}.xlsx",
        "log": f"{LOGS_DIR}/{base}.log"
    }
    return caminhos_arquivos
