from src.automation import coletar_dados
from src.names import gerar_caminhos_arquivos

def main():
    caminhos_arquivos = gerar_caminhos_arquivos()
    coletar_dados(caminhos_arquivos)

if __name__ == "__main__":
    main()
