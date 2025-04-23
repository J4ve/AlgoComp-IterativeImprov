import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges with capacities (our example: S, A, B, T)
# S is the server, T is the data center, A and B are intermediate routers

# We manually input the capacities based on the example:
# S → A: 10, S → B: 5
# A → B: 15
# A → T: 10, B → T: 10

edges = [
    ('S', 'A', 10),
    ('S', 'B', 5),
    ('A', 'B', 15),
    ('A', 'T', 10),
    ('B', 'T', 10)
]

# Add the edges and their capacities to the graph
for u, v, capacity in edges:
    G.add_edge(u, v, capacity=capacity)

# We use the Ford-Fulkerson algorithm (via Edmonds-Karp implementation in networkx)
# This is a classic example of iterative improvement: repeatedly find paths from S to T
# with residual capacity and push flow through the narrowest part of the path

# Compute maximum flow
flow_value, flow_dict = nx.maximum_flow(G, 'S', 'T')

# Display the flow result
print(f"Maximum Flow: {flow_value}")
print("Flow per edge:")
for u in flow_dict:
    for v in flow_dict[u]:
        print(f"{u} → {v}: {flow_dict[u][v]}")

# Visualization
pos = nx.spring_layout(G, seed=42)  # Positioning for consistent layout
edge_labels = {(u, v): f"{flow_dict[u][v]}/{G[u][v]['capacity']}" for u, v in G.edges()}

plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, node_size=2500, node_color="lightblue", font_weight="bold", arrows=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2, edge_color="gray")
plt.title("Network Graph with Flow / Capacity on Edges")
plt.axis("off")
plt.show()

