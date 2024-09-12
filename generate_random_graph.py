# Cria o grafo com o numero de nós e de arestas especificados
import random, sys

def generate_random_edges(num_nodes, num_edges):
    edges = set()
    
    # Step 1: Create a spanning tree to ensure the graph is connected
    nodes = list(range(1, num_nodes + 1))
    random.shuffle(nodes)  # Shuffle the nodes to create random connections
    
    # Add edges to form a spanning tree (n-1 edges)
    for i in range(1, num_nodes):
        u = nodes[i-1]
        v = nodes[i]
        edges.add((u, v) if u < v else (v, u))
    
    # Step 2: Add additional random edges to reach the desired number of edges
    while len(edges) < num_edges:
        u = random.randint(1, num_nodes)
        v = random.randint(1, num_nodes)
        
        if u != v:
            edge = (u, v) if u < v else (v, u)
            edges.add(edge)
    
    return edges

def write_edges_to_file(num_nodes, edges, filename):
    with open(filename, 'w') as file:
        file.write(f"{num_nodes}\n")
        for u, v in edges:
            file.write(f"{u} {v}\n")

 # Specify number of nodes and edges
num_nodes = 10
num_edges = 15  # Ensure this is at least (n - 1) for a connected graph

# Ensure the number of edges is valid
max_edges = num_nodes * (num_nodes - 1) // 2
if num_edges > max_edges:
    print(f"Too many edges. The maximum number of edges for {num_nodes} nodes is {max_edges}.")
    sys.exit()
if num_edges < num_nodes - 1:
    print(f"Too few edges. The minimum number of edges for {num_nodes} nodes to be connected is {num_nodes - 1}.")
    sys.exit()

# Generate random connected edges
edges = generate_random_edges(num_nodes, num_edges)

# Write edges to a file
filename = "grafo.txt"
write_edges_to_file(num_nodes, edges, filename)
print(f"Edges have been written to {filename}")