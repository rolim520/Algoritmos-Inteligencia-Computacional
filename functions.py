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
        edge = linha.split()
        if len(edge) == 3:
            a, b, w = edge
            # Convert to int if they are numbers, otherwise keep as strings
            a = int(a) if a.isdigit() else letter_to_int(a)
            b = int(b) if b.isdigit() else letter_to_int(b)
            w = int(w)

            matriz_adj[a-1][b-1] = w
            matriz_adj[b-1][a-1] = w
        else:
            a, b = edge
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

    G = nx.Graph()

    for linha in file:
        edge = linha.split()
        if len(edge) == 3:
            a, b, w = edge

            # Convert to int if they are numbers, otherwise keep as strings
            a = int(a) if a.isdigit() else a
            b = int(b) if b.isdigit() else b
            w = float(w)  # Assuming weights can be decimal, convert to float

            # Add the edge with weight to the graph
            G.add_edge(a, b, weight=w)
        else:
            a, b = linha.split()
            
            # Convert to int if they are numbers, otherwise keep as strings
            a = int(a) if a.isdigit() else a
            b = int(b) if a.isdigit() else b
            
            G.add_edge(a, b)  # If no weight, just add the edge without weight

    # Close the file
    file.close()

    # Use spring layout for better spacing
    pos = nx.spring_layout(G, k=0.5, iterations=50)  # Adjust 'k' for spacing

    # Draw the graph with the specified layout
    plt.figure(figsize=(10, 8))  # Adjust the figure size if needed
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=700, edge_color='gray')

    # Extract edge weights for labeling
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Graph from File with Edge Weights")
    plt.show()

# Retorna os vizinhos do node na matriz adjacencia. Começa em 0
def obter_vizinhos(node, matriz_adj):
    nodes = []
    # Obtem os vizinhos do nó
    for i in range(len(matriz_adj[node])):
        if matriz_adj[node][i] != 0:
            nodes.append(i)
    return nodes

