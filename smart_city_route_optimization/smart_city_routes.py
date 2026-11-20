"""
Smart City Route Optimization System
Dijkstra vs Bellman-Ford on a weighted graph of city locations.
"""

import heapq
import random
import time

INF = float("inf")


class CityGraph:
    """Weighted graph: locations are vertices, roads are weighted edges."""

    def __init__(self):
        self.adj = {}  # location -> list of (neighbor, weight)

    def add_location(self, name):
        self.adj.setdefault(name, [])

    def add_road(self, a, b, distance, two_way=True):
        self.add_location(a)
        self.add_location(b)
        self.adj[a].append((b, distance))
        if two_way:
            self.adj[b].append((a, distance))

    def locations(self):
        return list(self.adj)

    def edges(self):
        """Every directed edge as (u, v, w) - used by Bellman-Ford."""
        return [(u, v, w) for u in self.adj for v, w in self.adj[u]]


def _build_path(parent, source, target):
    path, node = [], target
    while node is not None:
        path.append(node)
        node = parent.get(node)
    path.reverse()
    return path if path and path[0] == source else []


def dijkstra(graph, source, target):
    """Min-heap Dijkstra. O((V + E) log V). Needs non-negative weights."""
    dist = {v: INF for v in graph.adj}
    parent = {source: None}
    dist[source] = 0
    heap = [(0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue  # stale entry
        if u == target:
            break
        for v, w in graph.adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                parent[v] = u
                heapq.heappush(heap, (dist[v], v))

    return dist[target], _build_path(parent, source, target)


def bellman_ford(graph, source, target):
    """Bellman-Ford. O(V * E). Handles negative weights, detects negative cycles."""
    dist = {v: INF for v in graph.adj}
    parent = {source: None}
    dist[source] = 0
    edges = graph.edges()

    for _ in range(len(graph.adj) - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
        if not changed:  # early exit
            break

    for u, v, w in edges:  # one more pass -> negative cycle check
        if dist[u] != INF and dist[u] + w < dist[v]:
            raise ValueError("Negative cycle detected")

    return dist[target], _build_path(parent, source, target)


def random_graph(n, avg_degree=4, seed=None):
    """Random connected city graph with n locations (L0..L{n-1})."""
    rng = random.Random(seed)
    g = CityGraph()
    names = [f"L{i}" for i in range(n)]
    for i in range(1, n):  # random spanning tree keeps it connected
        g.add_road(names[i], names[rng.randrange(i)], rng.randint(1, 100))
    for _ in range(n * (avg_degree - 2) // 2):  # extra roads
        a, b = rng.sample(names, 2)
        g.add_road(a, b, rng.randint(1, 100))
    return g


def benchmark(sizes=(50, 100, 200, 400, 800), runs=3, verbose=True):
    """Time both algorithms on random graphs. Returns [(n, edges, dij_ms, bf_ms)]."""
    results = []
    if verbose:
        print(f"{'Nodes':>7} {'Edges':>8} {'Dijkstra (ms)':>15} {'Bellman-Ford (ms)':>19}")
    for n in sizes:
        g = random_graph(n, seed=n)
        src, dst = "L0", f"L{n - 1}"
        times = {}
        for name, fn in (("dij", dijkstra), ("bf", bellman_ford)):
            best = INF
            for _ in range(runs):
                t = time.perf_counter()
                fn(g, src, dst)
                best = min(best, time.perf_counter() - t)
            times[name] = best * 1000
        results.append((n, len(g.edges()), times["dij"], times["bf"]))
        if verbose:
            print(f"{n:>7} {len(g.edges()):>8} {times['dij']:>15.3f} {times['bf']:>19.3f}")
    return results


def sample_city():
    """A small hand-made city. Returns (graph, positions for drawing)."""
    city = CityGraph()
    roads = [
        ("Railway Station", "Central Mall", 4), ("Railway Station", "City Hospital", 2),
        ("City Hospital", "Central Mall", 1), ("Central Mall", "University", 5),
        ("City Hospital", "Old Market", 3), ("Old Market", "Bus Terminal", 4),
        ("Central Mall", "Tech Park", 6), ("University", "Tech Park", 2),
        ("University", "Stadium", 4), ("Tech Park", "Airport", 7),
        ("Stadium", "Airport", 3), ("Bus Terminal", "Lake Park", 5),
        ("Lake Park", "Stadium", 6), ("Old Market", "Lake Park", 7),
        ("Bus Terminal", "Airport", 12),
    ]
    for a, b, d in roads:
        city.add_road(a, b, d)
    positions = {
        "Railway Station": (0, 3), "City Hospital": (1, 2), "Central Mall": (2, 3.5),
        "Old Market": (1, 0.5), "Bus Terminal": (2.6, 1.0), "University": (4, 3),
        "Tech Park": (4.5, 4.5), "Stadium": (5, 1.5), "Lake Park": (3.5, -0.5),
        "Airport": (6.5, 3.2),
    }
    return city, positions


def negative_weight_demo():
    """Shows Dijkstra failing on a negative edge while Bellman-Ford is correct."""
    g = CityGraph()
    g.add_road("A", "B", 4, two_way=False)
    g.add_road("A", "C", 5, two_way=False)
    g.add_road("C", "B", -3, two_way=False)  # toll refund / shortcut credit
    d1, p1 = dijkstra(g, "A", "B")
    d2, p2 = bellman_ford(g, "A", "B")
    print(f"Dijkstra     : {d1}  via {' -> '.join(p1)}   (WRONG - ignores the negative edge)")
    print(f"Bellman-Ford : {d2}  via {' -> '.join(p2)}   (correct)")

    cyc = CityGraph()
    cyc.add_road("A", "B", 1, two_way=False)
    cyc.add_road("B", "C", -2, two_way=False)
    cyc.add_road("C", "A", -1, two_way=False)  # cycle total = -2
    try:
        bellman_ford(cyc, "A", "C")
    except ValueError as e:
        print(f"Negative cycle test -> Bellman-Ford says: {e}")


def demo():
    city, _ = sample_city()
    src, dst = "Railway Station", "Airport"
    for name, fn in (("Dijkstra", dijkstra), ("Bellman-Ford", bellman_ford)):
        d, path = fn(city, src, dst)
        print(f"{name:13}: {d} km  via  {' -> '.join(path)}")


if __name__ == "__main__":
    print("=== Demo: shortest route ===")
    demo()
    print("\n=== Benchmark: random graphs ===")
    benchmark()
