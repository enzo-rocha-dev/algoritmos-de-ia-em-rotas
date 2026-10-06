# Script disponibilizado pelo professor para auxiliar na visualizacao da rota encontrada pelo grupo

import folium
import pandas as pd

# 1. O grupo carrega o arquivo de nos fornecido para pegar as latitudes e longitudes
nos_df = pd.read_csv("nos_ribeirao.csv", index_col='osmid')

# 2. Simulando o resultado do algoritmo de busca (uma lista de IDs de cruzamentos sequenciais)
# No codigo real, essa lista vem direto da execucao da busca escolhida pelo grupo
caminho_ids = [259576101, 618755937, 2236262014, 2405704515] # IDs ficticios para exemplo

# 3. Extrair as coordenadas geograficas correspondentes a esses IDs
caminho_coordenadas = []
for no_id in caminho_ids:
    if no_id in nos_df.index:
        lat = nos_df.loc[no_id, 'latitude']
        lon = nos_df.loc[no_id, 'longitude']
        caminho_coordenadas.append((lat, lon))

# 4. Criar o mapa centralizado no ponto de partida da busca
mapa = folium.Map(location=caminho_coordenadas[0], zoom_start=14)

# 5. Desenhar a rota no mapa (linha vermelha e grossa)
folium.PolyLine(
    locations=caminho_coordenadas,
    color='red',
    weight=5,
    opacity=0.8
).add_to(mapa)

# 6. (Opcional) Adicionar marcadores bonitinhos de Inicio e Fim
folium.Marker(caminho_coordenadas[0], popup="Origem", icon=folium.Icon(color="green")).add_to(mapa)
folium.Marker(caminho_coordenadas[-1], popup="Destino", icon=folium.Icon(color="red")).add_to(mapa)

# 7. Salvar o arquivo
mapa.save("rotaBuscaGrupoX.html")
print("Mapa de rota gerado com sucesso!")