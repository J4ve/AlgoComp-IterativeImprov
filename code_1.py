
"""
Simple Edmonds-Karp (Ford–Fulkerson with BFS) implementation
to compute the maximum flow in a network. 
Allows users to input custom graphs via the terminal.
"""
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def bfs(residual, source, sink, parent):
    """
    (Step 2b in pseudocode)
    We search the residual network for any S→T path with positive capacity.
    Here, we're using BFS to find the shortest such path (in terms of edges).
    """
    visited = [False] * len(residual)
    queue = deque([source])
    visited[source] = True
    parent[source] = -1  # mark the source's parent as undefined

    while queue:
        u = queue.popleft()
        # Explore neighbors of u in the residual graph
        for v, cap in enumerate(residual[u]):
            if not visited[v] and cap > 0:
                parent[v] = u
                visited[v] = True
                queue.append(v)
                if v == sink:
                    # (Step 2c) We've found an augmenting path
                    return True
    # No path found; can't push more flow
    return False

def edmonds_karp(capacity, source, sink):
    """
    Implements the iterative improvement loop.
    Corresponds directly to pseudocode Steps 1–3.
    """
    n = len(capacity)
    # (Step 1) Initialize all flows to zero by copying the initial capacity matrix
    residual = [row[:] for row in capacity]
    parent = [-1] * n
    max_flow = 0  # Total flow pushed so far

    # (Step 2) Repeat until no augmenting path remains
    while bfs(residual, source, sink, parent):
        # (Step 2d) Determine bottleneck capacity on the found path
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, residual[u][v])
            v = u

        # (Step 2e) Augment flow along the path by the bottleneck amount
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow  # reduce forward edge capacity
            residual[v][u] += path_flow  # increase reverse edge (undo flow) capacity
            v = u

        # Accumulate total flow
        max_flow += path_flow

    # (Step 3) Once no more paths exist, return the total maximum flow found
    return max_flow, [[capacity[u][v] - residual[u][v] for v in range(n)] for u in range(n)]

def read_graph():
    """
    Utility function to allow the user to input a custom graph.
    This doesn't directly map to pseudocode, but it's needed for testing the algorithm.
    """
    n = int(input("Enter the number of nodes in the network: "))
    print("Great! Now enter the capacity matrix, one row per line.")
    print(f"Each row should have {n} non-negative integers separated by spaces.")

    capacity = []
    for i in range(n):
        # Read each row of the capacity matrix
        row = list(map(int, input(f"Row {i} → ").strip().split()))
        if len(row) != n:
            raise ValueError(f"Row {i} must have exactly {n} entries.")
        capacity.append(row)

    # Define source and sink
    source = int(input(f"Enter the source node index (0 to {n-1}): "))
    sink = int(input(f"Enter the sink node index   (0 to {n-1}): "))

    return capacity, source, sink

#Here, we visualize the graph and max flow using NetworkX
def visualize_network(capacity, flow, source, sink):
    G = nx.DiGraph()
    n = len(capacity)

    # Add all edges with capacities and current flow values
    for u in range(n):
        for v in range(n):
            if capacity[u][v] > 0:
                label = f"{flow[u][v]}/{capacity[u][v]}" if flow[u][v] > 0 else f"0/{capacity[u][v]}"
                G.add_edge(u, v, label=label)

    pos = nx.spring_layout(G, seed=42)  # Positioning of nodes
    edge_labels = nx.get_edge_attributes(G, 'label')

    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=300)
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

    plt.title("Flow Network Visualization (flow/capacity)")
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    # Read graph input from user (not part of pseudocode but supports testing)
    cap_matrix, src, dst = read_graph()

    # Run the maximum flow algorithm
    print("\nComputing maximum flow...")
    maxflow, final_flow = edmonds_karp(cap_matrix, src, dst)

    # Output the result
    print(f"\nThe maximum possible flow from node {src} to node {dst} is: {maxflow}")
    visualize_network(cap_matrix, final_flow, src, dst)

