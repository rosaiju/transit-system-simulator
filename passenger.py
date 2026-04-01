def add_passengers(station, count):
    """Add passengers to a station's queue.

    Each passenger is represented as a string ID like 'P1', 'P2', etc.

    Args:
        station: Station object
        count: Number of passengers to add

    Returns:
        Number of passengers actually added (respects capacity).
    """
    current = len(station.passenger_queue)
    available = station.capacity - current

    if available <= 0:
        print(f"  {station.name} is at full capacity ({station.capacity}).")
        return 0

    to_add = min(count, available)

    # Generate unique passenger IDs based on current max
    existing_nums = []
    for p in station.passenger_queue:
        num = int(p.replace("P", ""))
        existing_nums.append(num)
    start_num = max(existing_nums) + 1 if existing_nums else 1

    for i in range(to_add):
        station.passenger_queue.append(f"P{start_num + i}")

    if to_add < count:
        print(f"  Added {to_add} passengers (capacity reached). "
              f"{count - to_add} turned away.")
    else:
        print(f"  Added {to_add} passengers to {station.name}.")

    return to_add


def board_passengers(station, count):
    """Board passengers from the front of the queue (FIFO).

    Args:
        station: Station object
        count: Number of passengers to board

    Returns:
        List of passenger IDs that boarded.
    """
    if not station.passenger_queue:
        print(f"  No passengers waiting at {station.name}.")
        return []

    to_board = min(count, len(station.passenger_queue))
    boarded = []

    for _ in range(to_board):
        passenger = station.passenger_queue.popleft()
        boarded.append(passenger)

    print(f"  Boarded {len(boarded)} passengers from {station.name}: "
          f"{', '.join(boarded)}")
    return boarded


def display_queue(station):
    """Display the current passenger queue at a station."""
    print(f"\n  Station: {station.name} (ID: {station.station_id})")
    print(f"  Capacity: {station.capacity}")
    print(f"  Passengers waiting: {len(station.passenger_queue)}")

    if station.passenger_queue:
        queue_str = ", ".join(station.passenger_queue)
        print(f"  Queue (front -> back): [{queue_str}]")
    else:
        print("  Queue: [empty]")
