import heapq
import math

def calcular_haversine(lat1, lon1, lat2, lon2):
    """Calcula a distância em metros entre duas coordenadas geográficas."""
    R = 6371000  # Raio médio da Terra em metros
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def haversine_a_star(origem, destino, grafo, coordenadas):
    """
    Executa o algoritmo A* para encontrar o caminho ótimo.
    Retorna: (caminho_lista_de_ids, distancia_total, nos_expandidos)
    """
    # Fila de prioridade: (f_score, g_score, osmid_atual, caminho_ate_aqui)
    fronteira = []
    heapq.heappush(fronteira, (0, 0, origem, [origem]))
    
    # Controle de custos já encontrados para evitar reprocessamento desnecessário
    custo_g_minimo = {origem: 0}
    
    nos_expandidos = 0
    lat_destino, lon_destino = coordenadas[destino]

    while fronteira:
        f_atual, g_atual, atual, caminho = heapq.heappop(fronteira)

        # Critério rigoroso do PDF: "O contador não incrementa nesta etapa porque o nó final é testado, não expandido"
        if atual == destino:
            return caminho, g_atual, nos_expandidos

        # Expansão do nó: Retirado da fronteira para avaliar os filhos
        nos_expandidos += 1

        # Otimização: ignora caminhos piores para um nó já visitado de forma mais eficiente
        if g_atual > custo_g_minimo.get(atual, float('inf')):
            continue

        for vizinho, distancia_aresta in grafo.get(atual, []):
            novo_g = g_atual + distancia_aresta
            
            if novo_g < custo_g_minimo.get(vizinho, float('inf')):
                custo_g_minimo[vizinho] = novo_g
                lat_viz, lon_viz = coordenadas[vizinho]
                h_score = calcular_haversine(lat_viz, lon_viz, lat_destino, lon_destino)
                f_score = novo_g + h_score
                
                novo_caminho = list(caminho)
                novo_caminho.append(vizinho)
                
                heapq.heappush(fronteira, (f_score, novo_g, vizinho, novo_caminho))

    return None, 0, nos_expandidos # Caso não encontre rota