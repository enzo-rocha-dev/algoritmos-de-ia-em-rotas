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
def haversine_a_star(origem, destino, grafo, coordenadas):
    #Executa o algoritmo A* para encontrar o caminho mais curto entre origem e destino. Utiliza a distância de Haversine como heurística (estimativa de custo).
    # A fronteira é uma lista que guarda os nós a serem explorados no formato:
    # (f_score, g_score, nó_atual, caminho_percorrido)
    fronteira = [(0, 0, origem, [origem])]
    
    # Dicionário para rastrear a menor distância real já encontrada até cada nó
    custo_g_minimo = {origem: 0}
    nos_expandidos = 0
    lat_destino, lon_destino = coordenadas[destino]

    while fronteira:
        # Pega o nó mais promissor da fronteira (menor custo total estimado)
        menor_indice = min(range(len(fronteira)), key=lambda i: fronteira[i][0])
        f_atual, g_atual, atual, caminho = fronteira.pop(menor_indice)

        # Condição de sucesso: chegamos ao destino
        if atual == destino:
            return caminho, g_atual, nos_expandidos

        nos_expandidos += 1

        # Ignora caminhos se já encontramos uma rota mais eficiente para este mesmo nó antes
        if g_atual > custo_g_minimo.get(atual, float('inf')):
            continue

        # Avalia os nós vizinhos (cruzamentos conectados pela rua)
        for vizinho, distancia_aresta in grafo.get(atual, []):
            novo_g = g_atual + distancia_aresta
            
            # Se o novo trajeto até o vizinho for melhor, atualizamos as rotas
            if novo_g < custo_g_minimo.get(vizinho, float('inf')):
                custo_g_minimo[vizinho] = novo_g
                
                lat_viz, lon_viz = coordenadas[vizinho]
                h_score = calcular_haversine(lat_viz, lon_viz, lat_destino, lon_destino)
                f_score = novo_g + h_score
                
                # Cria uma cópia do caminho percorrido até aqui e adiciona o vizinho
                novo_caminho = list(caminho)
                novo_caminho.append(vizinho)
                
                fronteira.append((f_score, novo_g, vizinho, novo_caminho))

    # Retorna vazio se esgotar as possibilidades sem encontrar o destino
    return None, 0, nos_expandidos