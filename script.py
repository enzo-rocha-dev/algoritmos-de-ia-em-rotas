# Integrantes do grupo:
# Enzo Rocha - 15449850
# Giovana Leite - 16869044
# Rafael Oliveira - 17152206

#importa as bibliotecas necessárias para a execução do código
import folium #biblioteca para geração dos gráficos
import pandas as pd #biblioteca para manipulação de dados

# Le os arquivos CSV contendo os dados dos nós e das arestas
nos_df = pd.read_csv("data/nos.csv", index_col='osmid') #coloca a colubna 'osmid' como índice do DataFrame
arestas_df = pd.read_csv("data/arestas.csv")

# Cria um dicionário com as coordenadas de cada nó: coordenadas[osmid] = (latitude, longitude)
coordenadas = {}
for osmid, linha in nos_df.iterrows():
    coordenadas[osmid] = (linha['latitude'], linha['longitude'])

# Cria o grafo como lista de adjacência: grafo[osmid] = {vizinho: distancia}
# A aresta é adicionada nos dois sentidos, pois o grafo é não orientado
grafo = {}
for linha in arestas_df.itertuples():
    if linha.origem not in grafo:
        grafo[linha.origem] = {}
    if linha.destino not in grafo:
        grafo[linha.destino] = {}
    grafo[linha.origem][linha.destino] = linha.distancia
    grafo[linha.destino][linha.origem] = linha.distancia

# Solicita ao usuário o ID de um cruzamento até ele digitar um válido
# Talvez em um futuro colocar a busca a partir do nome das ruas ao invés dos IDs (Não é obrigatório mas seria legal)
def ler_id(mensagem):
    while True:
        entrada = input(mensagem).strip()
        if not entrada.isdigit():
            print("Valor inválido. Digite apenas números.")
        elif int(entrada) not in coordenadas:
            print("Esse ID não existe na base de cruzamentos.")
        else:
            return int(entrada)

# Chama a função para ler os IDs de origem e destino
origem = ler_id("Digite o ID de origem: ")
destino = ler_id("Digite o ID de destino: ")
caminho_ids = [origem, destino]

# IDs ficticios para exemplo que foram disponibilizadas no verRota.py [259576101, 618755937, 2236262014, 2405704515] 

# Extrai as coordenadas geograficas correspondentes a esses IDs
caminho_coordenadas = []
for no_id in caminho_ids:
    if no_id in nos_df.index:
        lat = nos_df.loc[no_id, 'latitude']
        lon = nos_df.loc[no_id, 'longitude']
        caminho_coordenadas.append((lat, lon))

# Cria o mapa centralizado no ponto de partida da busca
mapa = folium.Map(location=caminho_coordenadas[0], zoom_start=14)

# Desenha a rota no mapa (linha vermelha e grossa)
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
# Silga EGR é o nome do grupo, então o arquivo HTML gerado será chamado "rotaBuscaGrupoEGR.html"
mapa.save("rotaBuscaGrupoEGR.html")
print("Mapa de rota gerado com sucesso!")