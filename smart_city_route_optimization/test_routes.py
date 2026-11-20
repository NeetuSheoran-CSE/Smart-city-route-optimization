"""Run:  python test_routes.py"""

from smart_city_routes import (
    CityGraph, dijkstra, bellman_ford, random_graph, sample_city, INF,
)


def test_sample_city():
    city, _ = sample_city()
    d1, p1 = dijkstra(city, "Railway Station", "Airport")
    d2, p2 = bellman_ford(city, "Railway Station", "Airport")
    assert d1 == d2 == 15
    assert p1[0] == "Railway Station" and p1[-1] == "Airport"


def test_algorithms_agree_on_random_graphs():
    for n in (10, 50, 200):
        for seed in range(5):
            g = random_graph(n, seed=seed)
            d1, _ = dijkstra(g, "L0", f"L{n - 1}")
            d2, _ = bellman_ford(g, "L0", f"L{n - 1}")
            assert d1 == d2, (n, seed, d1, d2)


def test_same_source_and_target():
    city, _ = sample_city()
    assert dijkstra(city, "Airport", "Airport") == (0, ["Airport"])
    assert bellman_ford(city, "Airport", "Airport") == (0, ["Airport"])


def test_unreachable():
    g = CityGraph()
    g.add_road("A", "B", 1)
    g.add_location("Island")
    d1, p1 = dijkstra(g, "A", "Island")
    d2, p2 = bellman_ford(g, "A", "Island")
    assert d1 == d2 == INF and p1 == p2 == []


def test_negative_edge():
    g = CityGraph()
    g.add_road("A", "B", 4, two_way=False)
    g.add_road("A", "C", 5, two_way=False)
    g.add_road("C", "B", -3, two_way=False)
    assert bellman_ford(g, "A", "B")[0] == 2
    assert dijkstra(g, "A", "B")[0] == 4  # Dijkstra gives the wrong answer


def test_negative_cycle():
    g = CityGraph()
    g.add_road("A", "B", 1, two_way=False)
    g.add_road("B", "C", -2, two_way=False)
    g.add_road("C", "A", -1, two_way=False)
    try:
        bellman_ford(g, "A", "C")
    except ValueError:
        return
    raise AssertionError("negative cycle not detected")


if __name__ == "__main__":
    tests = [v for k, v in dict(globals()).items() if k.startswith("test_")]
    for t in tests:
        t()
        print(f"PASS  {t.__name__}")
    print(f"\nAll {len(tests)} tests passed.")
