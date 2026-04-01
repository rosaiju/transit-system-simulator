import time
from collections import deque


def dfs(graph, start_id, visited=None):
    """Depth-First Search using recursion.

    Args:
        graph: TransitGraph instance
        start_id: Station ID to start from
        visited: Set of already-visited IDs (used internally for recursion)

    Returns:
        List of station IDs in DFS visit order.
    """
    if start_id not in graph.stations:
        print(f"  Station ID {start_id} not found.")
        return []

    if visited is None:
        visited = set()

    visited.add(start_id)
    result = [start_id]

    for neighbor_id, _weight in graph.get_neighbors(start_id):
        if neighbor_id not in visited:
            result.extend(dfs(graph, neighbor_id, visited))

    return result


def bfs(graph, start_id):
    """Breadth-First Search using a queue.

    Args:
        graph: TransitGraph instance
        start_id: Station ID to start from

    Returns:
        List of station IDs in BFS visit order.
    """
    if start_id not in graph.stations:
        print(f"  Station ID {start_id} not found.")
        return []

    visited = set()
    queue = deque([start_id])
    visited.add(start_id)
    result = []

    while queue:
        current_id = queue.popleft()
        result.append(current_id)

        for neighbor_id, _weight in graph.get_neighbors(current_id):
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                queue.append(neighbor_id)

    return result


def display_traversal(graph, order, label):
    """Pretty-print a traversal result."""
    if not order:
        print(f"  {label}: (empty)")
        return

    names = [graph.stations[sid].name for sid in order]
    print(f"\n  {label} traversal order:")
    print(f"  {' -> '.join(names)}")
    print(f"  Visited {len(order)} station(s)")


def compare_traversals(graph, start_id):
    """Run DFS and BFS from the same start, compare timing."""
    print(f"\n  Comparing DFS vs BFS from Station {start_id}...")
    print("  " + "-" * 40)

    # DFS timing
    t0 = time.perf_counter()
    dfs_order = dfs(graph, start_id)
    dfs_time = time.perf_counter() - t0

    # BFS timing
    t0 = time.perf_counter()
    bfs_order = bfs(graph, start_id)
    bfs_time = time.perf_counter() - t0

    display_traversal(graph, dfs_order, "DFS")
    display_traversal(graph, bfs_order, "BFS")

    print(f"\n  Performance Comparison:")
    print(f"  {'Algorithm':<12} {'Stations Visited':<20} {'Time (ms)':<15}")
    print(f"  {'-'*47}")
    print(f"  {'DFS':<12} {len(dfs_order):<20} {dfs_time*1000:.4f}")
    print(f"  {'BFS':<12} {len(bfs_order):<20} {bfs_time*1000:.4f}")
    print(f"\n  Both algorithms are O(V + E).")
    print(f"  DFS uses recursion (call stack), BFS uses a queue.")
