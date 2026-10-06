# Integrantes do grupo:
# Enzo Rocha - 15449850
# Giovana Leite - 16869044
# Rafael Oliveira - 17152206

#importa as bibliotecas necessárias para a execução do código
import folium
import pandas as pd

# Le os arquivos CSV contendo os dados dos nós e das arestas
nos_df = pd.read_csv("data/nos.csv", index_col='osmid')
arestas_df = pd.read_csv("data/arestas.csv")

# Solicita ao usuário os IDs dos cruzamentos que deseja incluir na rota
# Talvez em um futuro colocar a busca a partir do nome das ruas ao invés dos IDs
def ler_caminho_ids():
    entrada = input("Digite os IDs dos cruzamentos separados por vírgula: ")
    # Filta espaços em branco e converte para inteiros
    return [int(no_id.strip()) for no_id in entrada.split(',') if no_id.strip()]

# Chama a função para ler os IDs dos cruzamentos
caminho_ids = ler_caminho_ids()

# IDs ficticios para exemplo [259576101, 618755937, 2236262014, 2405704515] 

# Extrai as coordenadas geograficas correspondentes a esses IDs
caminho_coordenadas = []
for no_id in caminho_ids:
    if no_id in nos_df.index:
        lat = nos_df.loc[no_id, 'latitude']
        lon = nos_df.loc[no_id, 'longitude']
        caminho_coordenadas.append((lat, lon))

# Cria o mapa centralizado no ponto de partida da busca
mapa = folium.Map(location=caminho_coordenadas[0], zoom_start=14)

# 5. Desenha a rota no mapa (linha vermelha e grossa)
folium.PolyLine(
    locations=caminho_coordenadas,
    color='red',
    weight=5,
    opacity=0.8
).add_to(mapa)

# Adiciona marcadores bonitinhos de Inicio e Fim
folium.Marker(caminho_coordenadas[0], popup="Origem", icon=folium.Icon(color="green")).add_to(mapa)
folium.Marker(caminho_coordenadas[-1], popup="Destino", icon=folium.Icon(color="red")).add_to(mapa)

# Salva o arquivo em HTML para visualizacao
mapa.save("rotaBuscaGrupoEGR.html")
print("Mapa de rota gerado com sucesso!")