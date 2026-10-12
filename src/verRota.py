import folium
import pandas as pd

def gerar_html_rota(caminho_ids, arquivo_nos, arquivo_saida, cor_linha='red'):
    """
    Gera um mapa interativo em HTML destacando a rota encontrada.
    """
    # Carrega os nós do CSV apenas com colunas necessárias
    nos_df = pd.read_csv(arquivo_nos, index_col='osmid')

    caminho_coordenadas = []
    for no_id in caminho_ids:
        if no_id in nos_df.index:
            lat = nos_df.loc[no_id, 'latitude']
            lon = nos_df.loc[no_id, 'longitude']
            caminho_coordenadas.append((lat, lon))

    if not caminho_coordenadas:
        print(f"Erro: Nenhum nó válido encontrado para renderizar no mapa {arquivo_saida}.")
        return

    # Cria o mapa centralizado no ponto de partida
    mapa = folium.Map(location=caminho_coordenadas[0], zoom_start=14)

    # Desenha a rota no mapa
    folium.PolyLine(
        locations=caminho_coordenadas,
        color=cor_linha,
        weight=5,
        opacity=0.8
    ).add_to(mapa)

    # Adiciona marcadores de Início e Fim
    folium.Marker(caminho_coordenadas[0], popup="Origem", icon=folium.Icon(color="green")).add_to(mapa)
    folium.Marker(caminho_coordenadas[-1], popup="Destino", icon=folium.Icon(color="red", icon="info-sign")).add_to(mapa)

    # Salva o arquivo HTML
    mapa.save(arquivo_saida)