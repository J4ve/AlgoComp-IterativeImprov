import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(G, flow_dict=None, title=""):
    pos = nx.spring_layout(G)
    edge_labels = {}

    for u, v, d in G.edges(data=True):
        if flow_dict and u in flow_dict and v in flow_dict[u]:
            label = f"{flow_dict[u][v]}/{d['capacity']}"
        else:
            label = f"0/{d['capacity']}"
        edge_labels[(u, v)] = label

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=700, font_size=10, font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
    nx.draw_networkx_edges(G, pos, width=2, arrowstyle='-|>', arrowsize=20)
    plt.title(title)
    plt.axis("off")
    plt.show()

def max_flow_iterative_improvement(G, source, sink):
    # Initialize all flows to zero
    flow = {u: {v: 0 for v in G[u]} for u in G}

    def build_residual_graph():
        R = nx.DiGraph()
        for u in G:
            for v in G[u]:
                capacity = G[u][v]['capacity']
                residual = capacity - flow[u][v]
                if residual > 0:
                    R.add_edge(u, v, capacity=residual)
                if flow[u][v] > 0:
                    R.add_edge(v, u, capacity=flow[u][v])  # this allows us to undo flow
        return R

    while True:
        R = build_residual_graph()
        try:
            # Try finding an augmenting path—we thought of this as spotting a way to sneak more data through
            path = nx.shortest_path(R, source=source, target=sink)
        except nx.NetworkXNoPath:
            break  # If there's no more room, we stop here

        # Determine how much flow we can push through this path
        bottleneck = min(R[u][v]['capacity'] for u, v in zip(path, path[1:]))

        # Augment flow along the path—here we do the actual rerouting
        for u, v in zip(path, path[1:]):
            if G.has_edge(u, v):  # it's a forward edge
                flow[u][v] += bottleneck
            else:  # must be a backward edge, reducing flow
                flow[v][u] -= bottleneck

    # Once we’re done pushing, we total the outgoing flow from the source
    max_flow = sum(flow[source][v] for v in flow[source])
    return flow, max_flow

# Example usage
G = nx.DiGraph()

# Let's construct a simple network with capacities
edges = [
    ('S', 'A', 10),
    ('S', 'B', 5),
    ('A', 'B', 15),
    ('A', 'T', 10),
    ('B', 'T', 10)
]

for u, v, cap in edges:
    G.add_edge(u, v, capacity=cap)

# Visualize the initial state
draw_graph(G, title="Initial Network with Capacities")

# Run the iterative improvement algorithm
flow_result, maxflow = max_flow_iterative_improvement(G, 'S', 'T')

# Visualize the final state with flow values
draw_graph(G, flow_dict=flow_result, title=f"Final Flow - Max Flow: {maxflow}")
print("Max Flow:", maxflow)
