import csv
import time
from src.haversine_a_star import haversine_a_star
from src.weighted_a_star import weighted_a_star
from src.verRota import gerar_html_rota

ARQUIVO_NOS = "data/nos.csv"
ARQUIVO_ARESTAS = "data/arestas.csv"

def carregar_dados():
    coordenadas = {}
    grafo = {}

    # Carregar os nós
    with open(ARQUIVO_NOS, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            osmid = int(row['osmid'])
            lat = float(row['latitude'])
            lon = float(row['longitude'])
            coordenadas[osmid] = (lat, lon)
            grafo[osmid] = [] # Inicializa o grafo para todos os nós
            
    # Carregar as arestas (Grafo NÃO Orientado conforme PDF)
    with open(ARQUIVO_ARESTAS, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            origem = int(row['origem'])
            destino = int(row['destino'])
            distancia = float(row['distancia'])
            
            grafo[origem].append((destino, distancia))
            grafo[destino].append((origem, distancia)) # Não orientado = via de mão dupla
            
    return grafo, coordenadas

def main():
    print("Carregando mapa na memória...")
    grafo, coordenadas = carregar_dados()
    print("Dados carregados com sucesso!\n")

    # OSMIDs de teste (Substitua por nós que existam no arquivo da cidade)
    # Aqui utilizamos valores de teste fictícios para a estrutura rodar
    origem = list(coordenadas.keys())[0]
    destino = list(coordenadas.keys())[1000] # Pegando um nó arbitrário distante para o teste

    # ==========================
    # DESAFIO 1: A* Tradicional
    # ==========================
    cam_otimo, dist_otima, exp_otima = haversine_a_star(origem, destino, grafo, coordenadas)

    print("#" * 50)
    print("# RESULTADO DA BUSCA")
    print("#" * 50)
    print("DESAFIO 1 (ROTA ÓTIMA)")
    print(f"# Algoritmo utilizado: A* com Heurística de Haversine")
    print(f"# Origem (osmid): {origem}")
    print(f"# Destino (osmid): {destino}")
    print("#")
    
    if cam_otimo:
        print(f"# Caminho encontrado (Qtd nós): {len(cam_otimo)} cruzamentos")
        print(f"# Distância da Rota: {dist_otima:.2f} metros")
        print(f"# NÓS EXPANDIDOS: {exp_otima}")
        gerar_html_rota(cam_otimo, ARQUIVO_NOS, "rota_desafio_1_otima.html", cor_linha='blue')
    else:
        print("# NENHUM CAMINHO ENCONTRADO.")
    
    print("#" * 50)

    # ==========================
    # DESAFIO 2: Weighted A*
    # ==========================
    # O peso de 1.5 é um bom valor inicial para ganhar tempo cedendo um pouco da otimalidade
    cam_expresso, dist_expressa, exp_expressa = weighted_a_star(origem, destino, grafo, coordenadas, peso=1.5)

    print("DESAFIO 2 (ROTA EXPRESSA)")
    print(f"# Algoritmo utilizado: Weighted A* (Peso: 1.5)")
    print(f"# Origem (osmid): {origem}")
    print(f"# Destino (osmid): {destino}")
    print("#")
    
    if cam_expresso:
        # Cálculos de variação percentual em relação à rota ótima
        pct_dist = ((dist_expressa - dist_otima) / dist_otima) * 100 if dist_otima > 0 else 0
        pct_exp = ((exp_expressa - exp_otima) / exp_otima) * 100 if exp_otima > 0 else 0
        
        # Formatação de sinal para ficar igual ao PDF
        sinal_dist = "+" if pct_dist >= 0 else ""
        sinal_exp = "+" if pct_exp >= 0 else ""

        print(f"# Caminho encontrado (Qtd nós): {len(cam_expresso)} cruzamentos")
        print(f"# Distância da Rota: {dist_expressa:.2f} metros ({sinal_dist}{pct_dist:.2f}%)")
        print(f"# NÓS EXPANDIDOS: {exp_expressa} ({sinal_exp}{pct_exp:.2f}%)")
        gerar_html_rota(cam_expresso, ARQUIVO_NOS, "rota_desafio_2_expressa.html", cor_linha='orange')
    else:
        print("# NENHUM CAMINHO ENCONTRADO.")

    print("#" * 50)
    print("\n[+] Mapas HTML (rota_desafio_1_otima.html e rota_desafio_2_expressa.html) foram gerados com sucesso!")

if __name__ == "__main__":
    main()