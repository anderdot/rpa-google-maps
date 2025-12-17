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
