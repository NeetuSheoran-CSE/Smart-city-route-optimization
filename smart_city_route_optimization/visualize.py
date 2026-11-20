"""Charts and map drawing for the Smart City Route Optimization System."""

import matplotlib.pyplot as plt
import networkx as nx


def plot_benchmark(results, filename="benchmark.png", show=False):
    """results: [(nodes, edges, dijkstra_ms, bellman_ford_ms)]"""
    nodes = [r[0] for r in results]
    dij = [r[2] for r in results]
    bf = [r[3] for r in results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    ax1.plot(nodes, dij, "o-", label="Dijkstra", color="#2a9d8f")
    ax1.plot(nodes, bf, "s-", label="Bellman-Ford", color="#e76f51")
    ax1.set_title("Runtime vs graph size")
    ax1.set_xlabel("Number of locations (V)")
    ax1.set_ylabel("Time (ms)")
    ax1.grid(alpha=0.3)
    ax1.legend()

    ratio = [b / d if d else 0 for b, d in zip(bf, dij)]
    ax2.bar([str(n) for n in nodes], ratio, color="#264653")
    ax2.set_title("How many times slower is Bellman-Ford?")
    ax2.set_xlabel("Number of locations (V)")
    ax2.set_ylabel("Bellman-Ford time / Dijkstra time")
    ax2.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(filename, dpi=150)
    print(f"Chart saved: {filename}")
    if show:
        plt.show()
    plt.close(fig)


def draw_city(graph, positions, path=None, filename="route_map.png", title="City map", show=False):
    """Draw the city; highlight `path` (list of location names) if given."""
    G = nx.Graph()
    for u in graph.adj:
        for v, w in graph.adj[u]:
            G.add_edge(u, v, weight=w)

    pos = positions or nx.spring_layout(G, seed=7)
    fig, ax = plt.subplots(figsize=(11, 6.5))

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#bbbbbb", width=1.5)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color="#a8dadc", node_size=1500)
    on_path = set(path or [])

    if path and len(path) > 1:
        route_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=route_edges, edge_color="#e63946", width=4)
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=path, node_color="#ffb703", node_size=1500)
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=[path[0]], node_color="#2a9d8f", node_size=1700)
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=[path[-1]], node_color="#e63946", node_size=1700)

    nx.draw_networkx_edge_labels(
        G, pos, ax=ax, edge_labels=nx.get_edge_attributes(G, "weight"), font_size=8,
        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9),
    )
    nx.draw_networkx_labels(G, pos, ax=ax, labels={n: n for n in G if n not in on_path}, font_size=8)
    nx.draw_networkx_labels(G, pos, ax=ax, labels={n: n for n in on_path}, font_size=8, font_weight="bold")

    ax.set_title(title)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(filename, dpi=150)
    print(f"Map saved: {filename}")
    if show:
        plt.show()
    plt.close(fig)
