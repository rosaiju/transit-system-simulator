class ActionStack:
    """Stack-based undo system that records all actions for reversal."""

    def __init__(self):
        self._stack = []

    def push(self, action):
        """Push an action onto the stack.

        Args:
            action: dict with 'type' and 'data' keys.
                Types: 'add_station', 'remove_station',
                       'add_connection', 'remove_connection',
                       'board_passengers', 'add_passengers'
        """
        self._stack.append(action)

    def pop(self):
        """Pop the most recent action. Returns None if empty."""
        if self.is_empty():
            return None
        return self._stack.pop()

    def peek(self):
        """View the most recent action without removing it."""
        if self.is_empty():
            return None
        return self._stack[-1]

    def is_empty(self):
        return len(self._stack) == 0

    def size(self):
        return len(self._stack)

    def history(self):
        """Return full history list (oldest first)."""
        return list(self._stack)

    def undo(self, graph):
        """Pop the last action and reverse it on the graph.

        Returns a string describing what was undone, or None if nothing to undo.
        """
        action = self.pop()
        if action is None:
            return None

        action_type = action["type"]
        data = action["data"]

        if action_type == "add_station":
            # Reverse: remove the station that was added
            graph.remove_station(data["station_id"], record=False)
            return f"Undid add station '{data['name']}' (ID {data['station_id']})"

        elif action_type == "remove_station":
            # Reverse: re-add the station and its connections
            graph.add_station(
                data["station_id"], data["name"], data["capacity"], record=False
            )
            for neighbor_id, weight in data["connections"]:
                graph.add_connection(
                    data["station_id"], neighbor_id, weight, record=False
                )
            return f"Undid remove station '{data['name']}' (ID {data['station_id']})"

        elif action_type == "add_connection":
            # Reverse: remove the connection
            graph.remove_connection(data["id1"], data["id2"], record=False)
            return (
                f"Undid add connection between "
                f"Station {data['id1']} and Station {data['id2']}"
            )

        elif action_type == "remove_connection":
            # Reverse: re-add the connection
            graph.add_connection(
                data["id1"], data["id2"], data["weight"], record=False
            )
            return (
                f"Undid remove connection between "
                f"Station {data['id1']} and Station {data['id2']}"
            )

        elif action_type == "board_passengers":
            # Reverse: put passengers back in the queue
            station = graph.get_station(data["station_id"])
            if station:
                for p in data["boarded"]:
                    station.passenger_queue.appendleft(p)
            return (
                f"Undid boarding {len(data['boarded'])} passengers "
                f"at Station {data['station_id']}"
            )

        elif action_type == "add_passengers":
            # Reverse: remove passengers from the back of the queue
            station = graph.get_station(data["station_id"])
            if station:
                for _ in range(data["count"]):
                    if station.passenger_queue:
                        station.passenger_queue.pop()
            return (
                f"Undid adding {data['count']} passengers "
                f"at Station {data['station_id']}"
            )

        return None
