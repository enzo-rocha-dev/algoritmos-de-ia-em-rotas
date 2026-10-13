import csv
import time
from src.haversine_a_star import haversine_a_star
from src.weighted_a_star import weighted_a_star
from src.verRota import gerar_html_rota, gerar_html_comparacao

# Configurações de arquivos e parâmetros da busca
ARQUIVO_NOS = "data/nos.csv"
ARQUIVO_ARESTAS = "data/arestas.csv"
PESO_DE_HEURISTICA = 3

def carregar_dados():
    #Lê os arquivos CSV e os converte em estruturas de dados úteis na memória: um dicionário para as coordenadas e outro simulando o grafo de ruas.
    coordenadas = {}
    grafo = {}

    # Carrega os cruzamentos
    with open(ARQUIVO_NOS, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            osmid = int(row['osmid'])
            lat, lon = float(row['latitude']), float(row['longitude'])
            coordenadas[osmid] = (lat, lon)
            grafo[osmid] = []
            
    # Carrega as ruas (arestas bidirecionais) que conectam os cruzamentos
    with open(ARQUIVO_ARESTAS, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            origem = int(row['origem'])
            destino = int(row['destino'])
            distancia = float(row['distancia'])
            
            grafo[origem].append((destino, distancia))
            grafo[destino].append((origem, distancia))
            
    return grafo, coordenadas

def main():
    #Função orquestradora: Recebe inputs do usuário, processa ambas as buscas (A* e Weighted A*), exibe os comparativos e gera as representações gráficas.
    print("Carregando mapa na memória...")
    grafo, coordenadas = carregar_dados()
    print("Dados carregados com sucesso!\n")

    # Interação básica solicitando os pontos ao usuário
    origem = int(input("Digite o ID de origem: "))
    destino = int(input("Digite o ID de destino: "))

    # --- DESAFIO 1: A* TRADICIONAL ---
    cam_otimo, dist_otima, exp_otima = haversine_a_star(origem, destino, grafo, coordenadas)

    print(f"\n#{'-' * 50}")
    print("# RESULTADO DA BUSCA - DESAFIO 1 (ROTA ÓTIMA)")
    print(f"#{'-' * 50}")
    print(f"# Algoritmo utilizado: A* com Heurística de Haversine")
    print(f"# Origem (osmid): {origem} \n# Destino (osmid): {destino}")
    print(f"#{'-' * 50}")
    
    if cam_otimo:
        print(f"# Caminho encontrado (Qtd nós): {len(cam_otimo)} cruzamentos")
        print(f"# Distância da Rota: {dist_otima:.2f} metros")
        print(f"# NÓS EXPANDIDOS: {exp_otima}")
        gerar_html_rota(cam_otimo, ARQUIVO_NOS, "rota_desafio_1_otima.html", cor_linha='green')
    else:
        print("# NENHUM CAMINHO ENCONTRADO.")
    print(f"#{'-' * 50}\n")

    # --- DESAFIO 2: WEIGHTED A* (EXPRESSO) ---
    cam_expresso, dist_expressa, exp_expressa = weighted_a_star(origem, destino, grafo, coordenadas, peso=PESO_DE_HEURISTICA)

    print(f"#{'-' * 50}")
    print("# RESULTADO DA BUSCA - DESAFIO 2 (ROTA EXPRESSA)")
    print(f"#{'-' * 50}")
    print(f"# Algoritmo utilizado: Weighted A* (Peso: {PESO_DE_HEURISTICA})")
    print(f"# Origem (osmid): {origem} \n# Destino (osmid): {destino}")
    print(f"#{'-' * 50}")
    
    if cam_expresso:
        # Cálculos de eficiência e perdas para o console
        pct_dist = ((dist_expressa - dist_otima) / dist_otima) * 100 if dist_otima > 0 else 0
        pct_exp = ((exp_expressa - exp_otima) / exp_otima) * 100 if exp_otima > 0 else 0
        
        sinal_dist = "+" if pct_dist >= 0 else ""
        sinal_exp = "+" if pct_exp >= 0 else ""

        print(f"# Caminho encontrado (Qtd nós): {len(cam_expresso)} cruzamentos")
        print(f"# Distância da Rota: {dist_expressa:.2f} metros ({sinal_dist}{pct_dist:.2f}%)")
        print(f"# NÓS EXPANDIDOS: {exp_expressa} ({sinal_exp}{pct_exp:.2f}%)")
        gerar_html_rota(cam_expresso, ARQUIVO_NOS, "rota_desafio_2_expressa.html", cor_linha='red')
    else:
        print("# NENHUM CAMINHO ENCONTRADO.")
    print(f"#{'-' * 50}")

    # --- GERAÇÃO DO MAPA FINAL COMBINADO ---
    if cam_otimo and cam_expresso:
        print("\nGerando mapa comparativo com as duas rotas...")
        gerar_html_comparacao(cam_otimo, cam_expresso, ARQUIVO_NOS, "rotaBuscaGrupoEGR.html")

# Inicia a execução do programa
if __name__ == "__main__":
    main()