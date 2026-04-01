import time


def binary_search(sorted_stations, target_name):
    """Search for a station by name in a sorted list.

    Requires the list to be sorted by name alphabetically.

    Time: O(log n)
    Space: O(1)

    Returns the Station object or None.
    """
    low = 0
    high = len(sorted_stations) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_name = sorted_stations[mid].name.lower()
        target = target_name.lower()

        if mid_name == target:
            return sorted_stations[mid]
        elif mid_name < target:
            low = mid + 1
        else:
            high = mid - 1

    return None


def linear_search(stations, target_name):
    """Search for a station by name using linear scan.

    Time: O(n)
    Space: O(1)

    Returns the Station object or None.
    """
    target = target_name.lower()
    for station in stations:
        if station.name.lower() == target:
            return station
    return None


def compare_searches(stations, target_name):
    """Run both searches and compare their performance."""
    print(f"\n  Searching for station: '{target_name}'")
    print("  " + "-" * 40)

    # Sort by name for binary search
    sorted_by_name = sorted(stations, key=lambda s: s.name.lower())

    # Linear Search timing
    t0 = time.perf_counter()
    linear_result = linear_search(stations, target_name)
    linear_time = time.perf_counter() - t0

    # Binary Search timing (includes the sort as a separate note)
    t0 = time.perf_counter()
    binary_result = binary_search(sorted_by_name, target_name)
    binary_time = time.perf_counter() - t0

    if linear_result:
        print(f"  Linear Search found: {linear_result}")
    else:
        print(f"  Linear Search: not found")

    if binary_result:
        print(f"  Binary Search found: {binary_result}")
    else:
        print(f"  Binary Search: not found")

    print(f"\n  Performance Comparison ({len(stations)} stations):")
    print(f"  {'Algorithm':<18} {'Time Complexity':<18} {'Time (ms)':<15}")
    print(f"  {'-'*51}")
    print(f"  {'Linear Search':<18} {'O(n)':<18} {linear_time*1000:.4f}")
    print(f"  {'Binary Search':<18} {'O(log n)':<18} {binary_time*1000:.4f}")
    print(f"\n  Note: Binary Search requires sorted data (O(n log n) to sort first).")
    print(f"  For a single lookup, Linear Search may be faster overall.")
    print(f"  Binary Search excels when doing many lookups on the same sorted data.")
