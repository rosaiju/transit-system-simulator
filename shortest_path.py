import heapq


def dijkstra(graph, start_id, end_id):
    """Find the shortest path using Dijkstra's algorithm.

    Uses a min-heap (priority queue) to always process the closest
    unvisited station next.

    Args:
        graph: TransitGraph instance
        start_id: Starting station ID
        end_id: Destination station ID

    Returns:
        Tuple of (total_distance, path_list) where path_list is a list
        of station IDs from start to end. Returns (float('inf'), []) if
        no path exists.
    """
    if start_id not in graph.stations:
        print(f"  Station ID {start_id} not found.")
        return float("inf"), []
    if end_id not in graph.stations:
        print(f"  Station ID {end_id} not found.")
        return float("inf"), []

    # distances[station_id] = shortest known distance from start
    distances = {sid: float("inf") for sid in graph.stations}
    distances[start_id] = 0

    # previous[station_id] = previous station on shortest path
    previous = {sid: None for sid in graph.stations}

    # Min-heap entries: (distance, station_id)
    heap = [(0, start_id)]
    visited = set()

    while heap:
        current_dist, current_id = heapq.heappop(heap)

        if current_id in visited:
            continue
        visited.add(current_id)

        # Early exit if we reached the destination
        if current_id == end_id:
            break

        for neighbor_id, weight in graph.get_neighbors(current_id):
            if neighbor_id in visited:
                continue

            new_dist = current_dist + weight
            if new_dist < distances[neighbor_id]:
                distances[neighbor_id] = new_dist
                previous[neighbor_id] = current_id
                heapq.heappush(heap, (new_dist, neighbor_id))

    # Reconstruct path from end to start
    path = []
    current = end_id
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()

    # Check if a valid path was found
    if distances[end_id] == float("inf"):
        return float("inf"), []

    return distances[end_id], path


def display_shortest_path(graph, start_id, end_id):
    """Find and display the shortest path between two stations."""
    start_name = graph.stations[start_id].name if start_id in graph.stations else "?"
    end_name = graph.stations[end_id].name if end_id in graph.stations else "?"

    print(f"\n  Finding shortest path: {start_name} -> {end_name}")
    print("  " + "-" * 40)

    distance, path = dijkstra(graph, start_id, end_id)

    if not path:
        print(f"  No path exists between {start_name} and {end_name}.")
        return

    # Display the path with station names
    path_names = [graph.stations[sid].name for sid in path]
    print(f"  Path: {' -> '.join(path_names)}")
    print(f"  Total travel time: {distance} minutes")
    print(f"  Stops: {len(path) - 1}")

    # Show step-by-step breakdown
    print(f"\n  Step-by-step:")
    for i in range(len(path) - 1):
        from_name = graph.stations[path[i]].name
        to_name = graph.stations[path[i + 1]].name
        # Find the weight of this edge
        for nid, w in graph.get_neighbors(path[i]):
            if nid == path[i + 1]:
                print(f"    {from_name} --({w} min)--> {to_name}")
                break
