import time


def merge_sort(stations):
    """Sort stations by passenger capacity using Merge Sort.

    Time: O(n log n) — always
    Space: O(n) — creates new lists during merge

    Returns a new sorted list (does not mutate the original).
    """
    if len(stations) <= 1:
        return list(stations)

    mid = len(stations) // 2
    left = merge_sort(stations[:mid])
    right = merge_sort(stations[mid:])

    return _merge(left, right)


def _merge(left, right):
    """Merge two sorted lists into one sorted list."""
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i].capacity <= right[j].capacity:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def insertion_sort(stations):
    """Sort stations by passenger capacity using Insertion Sort.

    Time: O(n^2) worst/average, O(n) best (already sorted)
    Space: O(1) — sorts in-place on a copy

    Returns a new sorted list (does not mutate the original).
    """
    result = list(stations)

    for i in range(1, len(result)):
        key = result[i]
        j = i - 1

        while j >= 0 and result[j].capacity > key.capacity:
            result[j + 1] = result[j]
            j -= 1

        result[j + 1] = key

    return result


def display_sorted(stations, label):
    """Display a sorted list of stations."""
    print(f"\n  {label}:")
    print(f"  {'Rank':<6} {'Station':<20} {'Capacity':<10}")
    print(f"  {'-'*36}")
    for rank, station in enumerate(stations, 1):
        print(f"  {rank:<6} {station.name:<20} {station.capacity:<10}")


def compare_sorts(stations):
    """Run both sorts and compare their performance."""
    print("\n  Sorting stations by passenger capacity...")
    print("  " + "-" * 50)

    # Merge Sort timing
    t0 = time.perf_counter()
    merge_result = merge_sort(stations)
    merge_time = time.perf_counter() - t0

    # Insertion Sort timing
    t0 = time.perf_counter()
    insertion_result = insertion_sort(stations)
    insertion_time = time.perf_counter() - t0

    display_sorted(merge_result, "Merge Sort result")
    display_sorted(insertion_result, "Insertion Sort result")

    print(f"\n  Performance Comparison ({len(stations)} stations):")
    print(f"  {'Algorithm':<18} {'Time Complexity':<18} {'Time (ms)':<15}")
    print(f"  {'-'*51}")
    print(f"  {'Merge Sort':<18} {'O(n log n)':<18} {merge_time*1000:.4f}")
    print(f"  {'Insertion Sort':<18} {'O(n^2)':<18} {insertion_time*1000:.4f}")
    print(f"\n  Merge Sort is faster for large datasets.")
    print(f"  Insertion Sort can be faster for small/nearly-sorted data.")
