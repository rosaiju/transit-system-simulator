def load_demo_data(graph, action_stack=None):
    """Load a sample transit network with 12 stations and connections.

    Network layout (approximate):

        Station-1 --3-- Station-2 --4-- Station-3
            |               |               |
            2               5               3
            |               |               |
        Station-4 --6-- Station-5 --2-- Station-6
            |               |               |
            4               7               5
            |               |               |
        Station-7 --3-- Station-8 --4-- Station-9
                            |
                            6
                            |
                        Station-10 --3-- Station-11 --2-- Station-12
    """
    # Add 12 stations: (id, name, capacity)
    stations_data = [
        (1,  "Station-1",  100),
        (2,  "Station-2",  150),
        (3,  "Station-3",   80),
        (4,  "Station-4",  200),
        (5,  "Station-5",  300),
        (6,  "Station-6",  120),
        (7,  "Station-7",   90),
        (8,  "Station-8",  250),
        (9,  "Station-9",  110),
        (10, "Station-10", 180),
        (11, "Station-11",  70),
        (12, "Station-12", 160),
    ]

    for sid, name, capacity in stations_data:
        graph.add_station(sid, name, capacity, record=False)

    # Add weighted connections: (id1, id2, weight in minutes)
    connections_data = [
        # Row 1 horizontal
        (1, 2, 3),
        (2, 3, 4),
        # Row 2 horizontal
        (4, 5, 6),
        (5, 6, 2),
        # Row 3 horizontal
        (7, 8, 3),
        (8, 9, 4),
        # Bottom row horizontal
        (10, 11, 3),
        (11, 12, 2),
        # Column 1 vertical
        (1, 4, 2),
        (4, 7, 4),
        # Column 2 vertical
        (2, 5, 5),
        (5, 8, 7),
        # Column 3 vertical
        (3, 6, 3),
        (6, 9, 5),
        # Bridge to bottom row
        (8, 10, 6),
    ]

    for id1, id2, weight in connections_data:
        graph.add_connection(id1, id2, weight, record=False)

    # Add some passengers to a few stations for demo
    demo_passengers = {
        1: 5,
        5: 10,
        8: 8,
        12: 3,
    }

    for sid, count in demo_passengers.items():
        station = graph.get_station(sid)
        for i in range(1, count + 1):
            station.passenger_queue.append(f"P{i}")

    print("  Demo network loaded: 12 stations, 15 connections")
    print("  Passengers added to stations 1, 5, 8, and 12")
