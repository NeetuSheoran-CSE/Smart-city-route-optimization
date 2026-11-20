# Smart City Route Optimization System

Finds the shortest and most efficient route between locations in a city.
Locations are **vertices**, roads are **weighted edges** (distance in km).
Implements **Dijkstra** and **Bellman-Ford** from scratch and compares their performance.

## Setup
```
pip install matplotlib networkx
python main.py          # menu-driven program
python test_routes.py   # run the tests
```

## Files
| File | Purpose |
|---|---|
| `smart_city_routes.py` | Graph class, Dijkstra, Bellman-Ford, random graph generator, benchmark, negative-weight demo |
| `visualize.py` | Benchmark charts and city map with highlighted route (matplotlib + networkx) |
| `main.py` | Menu: view locations, find route, draw map, run benchmark, negative-weight demo |
| `test_routes.py` | Tests: both algorithms agree, unreachable nodes, negative edges and cycles |

## Data structure
Adjacency list (`dict: location -> [(neighbor, weight)]`). Space: O(V + E).

## Algorithms
| | Dijkstra | Bellman-Ford |
|---|---|---|
| Idea | Greedy: always expand the closest unvisited node (min-heap) | Relax every edge V-1 times |
| Time | O((V + E) log V) | O(V x E) |
| Space | O(V) | O(V) |
| Negative edges | Not supported (can give wrong answers) | Supported |
| Negative cycles | Not detected | Detected |
| Best for | Road networks (all distances positive) | Graphs with negative weights, cycle detection |

## Performance results
Random connected graphs, about 4 roads per location, best of 3 runs.
See `benchmark.png` (re-generate with menu option 4). Bellman-Ford grows much faster
with graph size, since it scans every edge repeatedly while Dijkstra only processes
each node once with a heap.

## Conclusion
- For normal city roads (distances are never negative), **Dijkstra is the right choice**: it is several times faster and the gap widens as the city grows.
- **Bellman-Ford** is slower but more general. It is needed when weights can be negative (for example toll refunds or incentives) and it can detect negative cycles.
- The negative-weight demo (menu option 5) shows Dijkstra returning 4 when the true shortest cost is 2.

## Possible extensions
Real map data (OpenStreetMap), traffic-based weights, A* search, a web UI with React.
