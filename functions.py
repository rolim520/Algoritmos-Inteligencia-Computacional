import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def letter_to_int(input_value):
    # If the input is a letter, return its alphabetical number
    if isinstance(input_value, str) and input_value.isalpha() and len(input_value) == 1:
        return ord(input_value.upper()) - 64  # 'A' is 65 in ASCII, so subtract 64 to get 1 for 'A'
    else:
        return "Invalid input! Please enter a letter (A-Z)"
    
def int_to_letter(input_value):
    # If the input is a number, return its respective letter
    if isinstance(input_value, int) and 1 <= input_value <= 26:
        return chr(input_value + 64)  # 'A' is 65 in ASCII, so add 64 to get 'A' for 1
    # Invalid input
    else:
        return "Invalid input! Please enter a number (1-26)."

def gerar_matriz_adjacente(path):
    file = open(path, "r")
    num_nodes = int(file.readline().strip())
    # Inicializa a matriz de adjacência
    matriz_adj = np.zeros((num_nodes, num_nodes))

    # Adiciona as arestas na matriz adjacência
    for linha in file:
        a, b = linha.split()
        # Convert to int if they are numbers, otherwise keep as strings
        a = int(a) if a.isdigit() else letter_to_int(a)
        b = int(b) if b.isdigit() else letter_to_int(b)

        matriz_adj[a-1][b-1] = 1
        matriz_adj[b-1][a-1] = 1

    return matriz_adj

def imprimir_resultado(descobertos, usarLetras=False):
    if usarLetras:
        print("Descobertos: ", list(map(int_to_letter, list(map(lambda x: x+1, descobertos)))))
    else:
        print("Descobertos: ", list(map(lambda x: x+1, descobertos)))

def visualizar_grafo(path):
    file = open(path, "r")
    num_nodes = int(file.readline().strip())
    edges = set()

    for linha in file:
        a, b = linha.split()
        
        # Convert to int if they are numbers, otherwise keep as strings
        a = int(a) if a.isdigit() else a
        b = int(b) if b.isdigit() else b
        
        edges.add((a, b))

    # Close the file
    file.close()

    G = nx.Graph()

    # Add edges to the graph
    G.add_edges_from(edges)

    # Use spring layout for better spacing
    pos = nx.spring_layout(G, k=0.5, iterations=50)  # Adjust 'k' for spacing, increase for more distance

    # Draw the graph with the specified layout
    plt.figure(figsize=(10, 8))  # Adjust the figure size if needed
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=700, edge_color='gray')
    plt.title("Graph from File")
    plt.show()

# Retorna os vizinhos do node na matriz adjacencia. Começa em 0
def obter_vizinhos(node, matriz_adj):
    nodes = []
    # Obtem os vizinhos do nó
    for i in range(len(matriz_adj[node])):
        if matriz_adj[node][i] == 1:
            nodes.append(i)
    return nodes

