# Integrantes do grupo:
# Enzo Rocha - 15449850
# Giovana Leite - 16869044
# Rafael Oliveira - 17152206

import math

def calcular_haversine(latitude_origem, longitude_origem, latitude_destino, longitude_destino):
    RAIO_DA_TERRA = 6371000 
    
    # Converte as coordenadas de graus para radianos
    lat_origem_rad, lat_destino_rad = math.radians(latitude_origem), math.radians(latitude_destino)
    diferenca_latitude_rad = math.radians(latitude_destino - latitude_origem)
    diferenca_longitude_rad = math.radians(longitude_destino - longitude_origem)
    
    # Aplica a formula trigonometrica para encontrar a distancia em metros
    proporcao_arco_esferico = math.sin(diferenca_latitude_rad / 2.0) ** 2 + math.cos(lat_origem_rad) * math.cos(lat_destino_rad) * math.sin(diferenca_longitude_rad / 2.0) ** 2
    angulo_central_radianos = 2 * math.atan2(math.sqrt(proporcao_arco_esferico), math.sqrt(1 - proporcao_arco_esferico))
    
    return RAIO_DA_TERRA * angulo_central_radianos

def weighted_a_star(origem, destino, grafo, coordenadas, peso):
    #Executa o algoritmo Weighted A* para encontrar caminhos mais rápidos computacionalmente.
    #A grande diferença é a aplicação de um 'peso' multiplicador na heurística, 
    #direcionando a busca mais rapidamente para o destino, sacrificando um pouco a rota ótima.
    fronteira = [(0, 0, origem, [origem])]
    custo_g_minimo = {origem: 0}
    nos_expandidos = 0
    lat_destino, lon_destino = coordenadas[destino]

    while fronteira:
        # Remove da lista o caminho com maior prioridade/menor custo
        menor_indice = min(range(len(fronteira)), key=lambda i: fronteira[i][0])
        f_atual, g_atual, atual, caminho = fronteira.pop(menor_indice)

        if atual == destino:
            return caminho, g_atual, nos_expandidos

        nos_expandidos += 1

        if g_atual > custo_g_minimo.get(atual, float('inf')):
            continue

        # Avaliações das ruas ligadas ao nó atual
        for vizinho, distancia_aresta in grafo.get(atual, []):
            novo_g = g_atual + distancia_aresta
            
            if novo_g < custo_g_minimo.get(vizinho, float('inf')):
                custo_g_minimo[vizinho] = novo_g
                
                lat_viz, lon_viz = coordenadas[vizinho]
                h_score = calcular_haversine(lat_viz, lon_viz, lat_destino, lon_destino)
                
                # INFLA a estimativa pelo fator do peso (Acelera o algoritmo)
                f_score = novo_g + (peso * h_score)
                
                novo_caminho = list(caminho)
                novo_caminho.append(vizinho)
                
                fronteira.append((f_score, novo_g, vizinho, novo_caminho))

    return None, 0, nos_expandidos