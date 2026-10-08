# Trabalho 1 - Algoritimos de IA para geração de rotas na cidade de Ribeirão Preto

## Objetivo do Projeto



## Biblioteca necessárias para execução do código
|Biblioteca | Objetivo  | Comanda de instalação |
|-----------|-----------|-----------------------|
| Folium |Biblioteca que facilita a criação de mapas interativos| `pip install folium` |
| Pandas | Biblioteca para manipualção de dados | `pip install pandas` |


## Como compilar e executar

Python é interpretado, então não há etapa de compilação. Basta ter o **Python 3** instalado e seguir os passos abaixo.

1. Instale as dependências:

   ```bash
   pip install folium pandas
   ```

2. Confira se os arquivos de dados estão na pasta `data/`:

   - `data/nos.csv`: cruzamentos (`osmid`, `latitude`, `longitude`)
   - `data/arestas.csv`: ruas entre cruzamentos (`origem`, `destino`, `distancia`, `nome_rua`)

3. Execute o script **a partir da raiz do projeto** (os caminhos dos CSVs são relativos a ela):

   ```bash
   python script.py
   ```

4. Quando solicitado, digite o ID (`osmid`) do cruzamento de origem e depois o de destino. Os IDs precisam existir em `data/nos.csv`. Exemplo:

   ```
   Digite o ID de origem: 259576101
   Digite o ID de destino: 2405704515
   ```

5. Ao final, o script gera o arquivo `rotaBuscaGrupoEGR.html` na raiz do projeto. Abra-o no navegador para ver a rota no mapa (origem em verde, destino em vermelho).



## Contexto e informações sobre o trabalho

Trabalho da disciplina **Inteligência Artificial**, ministrada pelo Prof. Dr. José Augusto Baranauskas (DCM/USP Ribeirão Preto), cujo enunciado completo está em [IA-Trabalho-2026-Ribeirao.pdf](documents/IA-Trabalho-2026-Ribeirao.pdf).

### Membros do grupo:

- Enzo Rocha - 15449850
- Giovana Leite - 16869044
- Rafael Oliveira - 17152206

Alunos do curso de Ciência da Computação da USP Ribeirão Preto.
