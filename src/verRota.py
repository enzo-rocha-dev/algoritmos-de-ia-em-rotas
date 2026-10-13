import folium
import pandas as pd

def gerar_html_rota(caminho_ids, arquivo_nos, arquivo_saida, cor_linha='red'):
    #Gera um mapa interativo em HTML mostrando uma rota específica. Cruza os IDs gerados pelo algoritmo com as coordenadas geográficas do CSV.
    nos_df = pd.read_csv(arquivo_nos, index_col='osmid')
    caminho_coordenadas = []
    
    # Extrai a latitude e longitude para cada nó do trajeto
    for no_id in caminho_ids:
        if no_id in nos_df.index:
            lat = nos_df.loc[no_id, 'latitude']
            lon = nos_df.loc[no_id, 'longitude']
            caminho_coordenadas.append((lat, lon))

    if not caminho_coordenadas:
        print(f"Erro: Nenhum nó válido encontrado para renderizar no mapa {arquivo_saida}.")
        return

    # Inicializa o mapa centralizado no ponto de partida da rota
    mapa = folium.Map(location=caminho_coordenadas[0], zoom_start=14)

    # Desenha o trajeto no mapa
    folium.PolyLine(locations=caminho_coordenadas, color=cor_linha, weight=5, opacity=0.8).add_to(mapa)

    # Adiciona os marcadores visuais de Origem e Destino
    folium.Marker(caminho_coordenadas[0], popup="Origem", icon=folium.Icon(color="green")).add_to(mapa)
    folium.Marker(caminho_coordenadas[-1], popup="Destino", icon=folium.Icon(color="red", icon="info-sign")).add_to(mapa)

    mapa.save(arquivo_saida)

def gerar_html_comparacao(caminho_otimo_ids, caminho_expresso_ids, arquivo_nos, arquivo_saida="rota_comparacao.html"):
    #Gera um mapa HTML sobrepondo duas rotas diferentes (a ótima e a expressa) para permitir a comparação visual do desempenho dos algoritmos.
    nos_df = pd.read_csv(arquivo_nos, index_col='osmid')

    def obter_coordenadas(ids):
        # Função auxiliar para mapear uma lista de IDs em coordenadas reais
        coords = []
        for no_id in ids:
            if no_id in nos_df.index:
                lat = nos_df.loc[no_id, 'latitude']
                lon = nos_df.loc[no_id, 'longitude']
                coords.append((lat, lon))
        return coords

    coords_otimo = obter_coordenadas(caminho_otimo_ids)
    coords_expresso = obter_coordenadas(caminho_expresso_ids)

    if not coords_otimo:
        print(f"Erro: Nenhum nó válido encontrado para a rota ótima em {arquivo_saida}.")
        return

    # Cria o mapa centralizado no início da rota ótima
    mapa = folium.Map(location=coords_otimo[0], zoom_start=14)

    # Plota a rota ótima na cor verde
    if coords_otimo:
        folium.PolyLine(
            locations=coords_otimo, color='green', weight=5, opacity=0.8, tooltip='Rota Ótima (A* Tradicional)'
        ).add_to(mapa)

    # Plota a rota expressa na cor vermelha (mais fina para não cobrir totalmente a verde)
    if coords_expresso:
        folium.PolyLine(
            locations=coords_expresso, color='red', weight=3, opacity=0.8, tooltip='Rota Expressa (Weighted A*)'
        ).add_to(mapa)

    # Marcadores de início e fim padronizados
    folium.Marker(coords_otimo[0], popup="Origem", icon=folium.Icon(color="green", icon="play")).add_to(mapa)
    folium.Marker(coords_otimo[-1], popup="Destino", icon=folium.Icon(color="red", icon="stop")).add_to(mapa)

    mapa.save(arquivo_saida)