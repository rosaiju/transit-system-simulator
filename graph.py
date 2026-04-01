from station import Station


class TransitGraph:
    """Weighted undirected graph using adjacency list representation."""

    def __init__(self):
        # station_id -> Station object
        self.stations = {}
        # station_id -> [(neighbor_id, weight), ...]
        self.adjacency_list = {}

    # ---- Station Operations ----

    def add_station(self, station_id, name, capacity, record=True):
        """Add a new station to the network.

        Args:
            record: If True, the caller is responsible for recording undo.
                    Internal undo calls pass record=False.
        """
        if station_id in self.stations:
            print(f"  Station ID {station_id} already exists.")
            return False

        self.stations[station_id] = Station(station_id, name, capacity)
        self.adjacency_list[station_id] = []
        return True

    def remove_station(self, station_id, record=True):
        """Remove a station and all its connections.

        Returns the removed station's data (for undo) or None.
        """
        if station_id not in self.stations:
            print(f"  Station ID {station_id} not found.")
            return None

        station = self.stations[station_id]
        # Save connections before removal (for undo)
        connections = list(self.adjacency_list[station_id])

        # Remove all edges pointing to this station
        for neighbor_id, _weight in connections:
            self.adjacency_list[neighbor_id] = [
                (nid, w)
                for nid, w in self.adjacency_list[neighbor_id]
                if nid != station_id
            ]

        # Remove the station itself
        del self.adjacency_list[station_id]
        del self.stations[station_id]

        return {
            "station_id": station.station_id,
            "name": station.name,
            "capacity": station.capacity,
            "connections": connections,
        }

    # ---- Connection Operations ----

    def add_connection(self, id1, id2, weight, record=True):
        """Add a weighted undirected edge between two stations."""
        if id1 not in self.stations:
            print(f"  Station ID {id1} not found.")
            return False
        if id2 not in self.stations:
            print(f"  Station ID {id2} not found.")
            return False

        # Check if connection already exists
        for neighbor_id, _w in self.adjacency_list[id1]:
            if neighbor_id == id2:
                print(f"  Connection already exists between {id1} and {id2}.")
                return False

        self.adjacency_list[id1].append((id2, weight))
        self.adjacency_list[id2].append((id1, weight))
        return True

    def remove_connection(self, id1, id2, record=True):
        """Remove the edge between two stations.

        Returns the weight of the removed edge (for undo) or None.
        """
        if id1 not in self.stations or id2 not in self.stations:
            print("  One or both station IDs not found.")
            return None

        weight = None
        for neighbor_id, w in self.adjacency_list[id1]:
            if neighbor_id == id2:
                weight = w
                break

        if weight is None:
            print(f"  No connection between {id1} and {id2}.")
            return None

        self.adjacency_list[id1] = [
            (nid, w) for nid, w in self.adjacency_list[id1] if nid != id2
        ]
        self.adjacency_list[id2] = [
            (nid, w) for nid, w in self.adjacency_list[id2] if nid != id1
        ]
        return weight

    # ---- Query Operations ----

    def get_station(self, station_id):
        """Look up a station by ID. Returns None if not found."""
        return self.stations.get(station_id)

    def get_all_stations(self):
        """Return a list of all Station objects."""
        return list(self.stations.values())

    def get_neighbors(self, station_id):
        """Return list of (neighbor_id, weight) for a station."""
        return self.adjacency_list.get(station_id, [])

    def station_count(self):
        return len(self.stations)

    def edge_count(self):
        """Each undirected edge is stored twice, so divide by 2."""
        total = sum(len(edges) for edges in self.adjacency_list.values())
        return total // 2

    # ---- Display ----

    def display_network(self):
        """Print the full network as an adjacency list."""
        if not self.stations:
            print("  Network is empty.")
            return

        print(f"\n  Transit Network ({self.station_count()} stations, "
              f"{self.edge_count()} connections)")
        print("  " + "-" * 50)

        for sid in sorted(self.adjacency_list.keys()):
            station = self.stations[sid]
            neighbors = self.adjacency_list[sid]

            if neighbors:
                connections_str = ", ".join(
                    f"{self.stations[nid].name} ({w} min)"
                    for nid, w in neighbors
                )
            else:
                connections_str = "(no connections)"

            print(f"  {station.name} [ID:{sid}, cap:{station.capacity}] "
                  f"-> {connections_str}")

        print("  " + "-" * 50)
