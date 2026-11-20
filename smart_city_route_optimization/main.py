"""
Smart City Route Optimization System - menu-driven program.
Run:  python main.py
"""

import time

from smart_city_routes import (
    sample_city, dijkstra, bellman_ford, benchmark, negative_weight_demo,
)
from visualize import draw_city, plot_benchmark


def pick_location(city, prompt):
    names = city.locations()
    while True:
        choice = input(prompt).strip()
        if choice.isdigit() and 1 <= int(choice) <= len(names):
            return names[int(choice) - 1]
        if choice in names:
            return choice
        print("  Invalid choice, enter a number from the list or the exact name.")


def show_locations(city):
    print("\nLocations:")
    for i, name in enumerate(city.locations(), 1):
        print(f"  {i:>2}. {name}")


def find_route(city, positions):
    show_locations(city)
    src = pick_location(city, "\nSource (number or name): ")
    dst = pick_location(city, "Destination (number or name): ")

    results = {}
    for name, fn in (("Dijkstra", dijkstra), ("Bellman-Ford", bellman_ford)):
        t = time.perf_counter()
        dist, path = fn(city, src, dst)
        results[name] = (dist, path, (time.perf_counter() - t) * 1000)

    print(f"\nShortest route from {src} to {dst}")
    for name, (dist, path, ms) in results.items():
        if not path:
            print(f"  {name:13}: no route exists")
            continue
        print(f"  {name:13}: {dist} km in {ms:.4f} ms")
        print(f"  {'':13}  {' -> '.join(path)}")

    path = results["Dijkstra"][1]
    if path:
        draw_city(city, positions, path, "route_map.png",
                  title=f"Shortest route: {src} to {dst} ({results['Dijkstra'][0]} km)",
                  show=True)


def run_benchmark():
    sizes = (50, 100, 200, 400, 800, 1600)
    print("\nRunning benchmark on random graphs (about 4 roads per location)...\n")
    data = benchmark(sizes)
    plot_benchmark(data, "benchmark.png", show=True)


def main():
    city, positions = sample_city()
    menu = """
==== Smart City Route Optimization System ====
 1. Show city locations
 2. Find shortest route (Dijkstra vs Bellman-Ford)
 3. Draw full city map
 4. Run performance benchmark + chart
 5. Negative-weight / negative-cycle demo
 0. Exit
"""
    while True:
        print(menu)
        choice = input("Choose an option: ").strip()
        if choice == "1":
            show_locations(city)
        elif choice == "2":
            find_route(city, positions)
        elif choice == "3":
            draw_city(city, positions, None, "city_map.png", "Smart City Road Network", show=True)
        elif choice == "4":
            run_benchmark()
        elif choice == "5":
            print()
            negative_weight_demo()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
