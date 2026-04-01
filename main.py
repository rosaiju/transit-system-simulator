from graph import TransitGraph
from undo_stack import ActionStack
from traversal import dfs, bfs, display_traversal, compare_traversals
from shortest_path import display_shortest_path
from passenger import add_passengers, board_passengers, display_queue
from sorting import compare_sorts
from searching import compare_searches
from demo_data import load_demo_data


def print_menu():
    print("\n" + "=" * 50)
    print("       TRANSIT SYSTEM SIMULATOR")
    print("=" * 50)
    print("  1.  Display Network")
    print("  2.  Add Station")
    print("  3.  Remove Station")
    print("  4.  Add Connection")
    print("  5.  Remove Connection")
    print("  6.  DFS Traversal")
    print("  7.  BFS Traversal")
    print("  8.  Compare DFS vs BFS")
    print("  9.  Find Shortest Path (Dijkstra)")
    print("  10. Add Passengers to Station")
    print("  11. Board Passengers")
    print("  12. View Station Queue")
    print("  13. Sort Stations by Capacity")
    print("  14. Search for Station")
    print("  15. Undo Last Action")
    print("  16. View Action History")
    print("  0.  Exit")
    print("=" * 50)


def get_int(prompt):
    """Safely read an integer from user input."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("  Please enter a valid number.")


def main():
    graph = TransitGraph()
    stack = ActionStack()

    # Auto-load demo data
    print("\n  Loading demo transit network...")
    load_demo_data(graph, stack)

    while True:
        print_menu()
        choice = get_int("  Enter choice: ")

        if choice == 0:
            print("\n  Goodbye!")
            break

        elif choice == 1:
            # Display Network
            graph.display_network()

        elif choice == 2:
            # Add Station
            sid = get_int("  Enter station ID: ")
            name = input("  Enter station name: ").strip()
            capacity = get_int("  Enter passenger capacity: ")

            if graph.add_station(sid, name, capacity):
                stack.push({
                    "type": "add_station",
                    "data": {
                        "station_id": sid,
                        "name": name,
                        "capacity": capacity,
                    },
                })
                print(f"  Station '{name}' added successfully.")

        elif choice == 3:
            # Remove Station
            sid = get_int("  Enter station ID to remove: ")
            removed = graph.remove_station(sid)
            if removed:
                stack.push({
                    "type": "remove_station",
                    "data": removed,
                })
                print(f"  Station '{removed['name']}' removed.")

        elif choice == 4:
            # Add Connection
            id1 = get_int("  Enter first station ID: ")
            id2 = get_int("  Enter second station ID: ")
            weight = get_int("  Enter travel time (minutes): ")

            if graph.add_connection(id1, id2, weight):
                stack.push({
                    "type": "add_connection",
                    "data": {"id1": id1, "id2": id2, "weight": weight},
                })
                s1 = graph.stations[id1].name
                s2 = graph.stations[id2].name
                print(f"  Connection added: {s1} <-> {s2} ({weight} min)")

        elif choice == 5:
            # Remove Connection
            id1 = get_int("  Enter first station ID: ")
            id2 = get_int("  Enter second station ID: ")

            weight = graph.remove_connection(id1, id2)
            if weight is not None:
                stack.push({
                    "type": "remove_connection",
                    "data": {"id1": id1, "id2": id2, "weight": weight},
                })
                print(f"  Connection removed.")

        elif choice == 6:
            # DFS Traversal
            sid = get_int("  Enter starting station ID: ")
            order = dfs(graph, sid)
            display_traversal(graph, order, "DFS")

        elif choice == 7:
            # BFS Traversal
            sid = get_int("  Enter starting station ID: ")
            order = bfs(graph, sid)
            display_traversal(graph, order, "BFS")

        elif choice == 8:
            # Compare DFS vs BFS
            sid = get_int("  Enter starting station ID: ")
            compare_traversals(graph, sid)

        elif choice == 9:
            # Shortest Path (Dijkstra)
            start = get_int("  Enter start station ID: ")
            end = get_int("  Enter destination station ID: ")
            display_shortest_path(graph, start, end)

        elif choice == 10:
            # Add Passengers
            sid = get_int("  Enter station ID: ")
            station = graph.get_station(sid)
            if station is None:
                print(f"  Station ID {sid} not found.")
            else:
                count = get_int("  How many passengers to add? ")
                added = add_passengers(station, count)
                if added > 0:
                    stack.push({
                        "type": "add_passengers",
                        "data": {"station_id": sid, "count": added},
                    })

        elif choice == 11:
            # Board Passengers
            sid = get_int("  Enter station ID: ")
            station = graph.get_station(sid)
            if station is None:
                print(f"  Station ID {sid} not found.")
            else:
                count = get_int("  How many passengers to board? ")
                boarded = board_passengers(station, count)
                if boarded:
                    stack.push({
                        "type": "board_passengers",
                        "data": {"station_id": sid, "boarded": boarded},
                    })

        elif choice == 12:
            # View Station Queue
            sid = get_int("  Enter station ID: ")
            station = graph.get_station(sid)
            if station is None:
                print(f"  Station ID {sid} not found.")
            else:
                display_queue(station)

        elif choice == 13:
            # Sort Stations by Capacity
            all_stations = graph.get_all_stations()
            if not all_stations:
                print("  No stations in the network.")
            else:
                compare_sorts(all_stations)

        elif choice == 14:
            # Search for Station
            target = input("  Enter station name to search: ").strip()
            all_stations = graph.get_all_stations()
            if not all_stations:
                print("  No stations in the network.")
            else:
                compare_searches(all_stations, target)

        elif choice == 15:
            # Undo Last Action
            if stack.is_empty():
                print("  Nothing to undo.")
            else:
                result = stack.undo(graph)
                if result:
                    print(f"  {result}")

        elif choice == 16:
            # View Action History
            history = stack.history()
            if not history:
                print("  No actions recorded.")
            else:
                print(f"\n  Action History ({len(history)} actions):")
                print("  " + "-" * 40)
                for i, action in enumerate(history, 1):
                    print(f"  {i}. {action['type']}: {action['data']}")

        else:
            print("  Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
