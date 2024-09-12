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

import networkx as nx
import matplotlib.pyplot as plt

def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    """
    If the graph is a tree, this will return the positions to plot this in a
    hierarchical layout.

    G: the graph (must be a tree)
    root: the root node of the current branch
    width: horizontal space allocated for this branch
    vert_gap: gap between levels of the hierarchy
    vert_loc: vertical location of root
    xcenter: horizontal location of root
    """

    pos = {root: (xcenter, vert_loc)}
    neighbors = list(G.neighbors(root))
    if len(neighbors) != 0:
        dx = width / len(neighbors) 
        nextx = xcenter - width / 2 - dx / 2
        for neighbor in neighbors:
            nextx += dx
            pos.update(hierarchy_pos(G, root=neighbor, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap, xcenter=nextx))
    return pos

def visualizar_arvore_de_pais(matriz_adj, pais):
    G = nx.DiGraph()  # Use directed graph to preserve parent-child hierarchy

    # Create edges for each child-parent relationship
    for filho in pais.keys():
        G.add_edge(pais[filho], filho, weight=matriz_adj[letter_to_int(pais[filho])-1][letter_to_int(filho)-1])

    # Find the root (the node with no parent)
    root = [node for node in G.nodes if node not in pais.keys()][0]

    # Get the hierarchical position layout
    pos = hierarchy_pos(G, root)

    # Draw the graph with the specified layout
    plt.figure(figsize=(10, 8))  # Adjust the figure size if needed
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=700, edge_color='gray')

    plt.title("Hierarchical Parent-Child Tree")
    plt.show()

# Retorna os vizinhos do node na matriz adjacencia. Começa em 0
def obter_vizinhos(node, matriz_adj):
    nodes = []
    # Obtem os vizinhos do nó
    for i in range(len(matriz_adj[node])):
        if matriz_adj[node][i] != 0:
            nodes.append(i)
    return nodes

def obter_indice_menor_distancia(abertos, distancia):
    min_dist_idx = 0
    for i in range(len(abertos)):
        if distancia[abertos[i]] < distancia[abertos[min_dist_idx]]:
            min_dist_idx = i
    return min_dist_idx

# Retorna se um dado vertice é conexo ao grafo
def conexo_ao_grafo(node, matriz_adj):
    for i in range(len(matriz_adj[node])):
        if matriz_adj[node][i] != 0:
            return True
    return False