from collections import deque


class Station:
    """Represents a transit station in the network."""

    def __init__(self, station_id, name, capacity):
        self.station_id = station_id
        self.name = name
        self.capacity = capacity
        self.passenger_queue = deque()

    def __repr__(self):
        return (
            f"Station({self.station_id}, '{self.name}', "
            f"capacity={self.capacity}, passengers={len(self.passenger_queue)})"
        )

    def __lt__(self, other):
        """Compare by capacity — used for sorting."""
        return self.capacity < other.capacity

    def __eq__(self, other):
        if not isinstance(other, Station):
            return False
        return self.station_id == other.station_id

    def __hash__(self):
        return hash(self.station_id)
