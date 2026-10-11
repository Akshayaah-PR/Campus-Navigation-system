"""
NCERC CAMPUS NAVIGATION SYSTEM
Shortest Path Algorithm using Dijkstra's Algorithm
"""

import heapq

from graph import campus_graph, locations


def find_shortest_path(start, destination):
    """
    Find the shortest logical route between two locations.

    Returns:
        path: List of locations in the route.
        error: Error message if a route cannot be found.
    """

    # Check whether the starting location exists.
    if start not in campus_graph:
        return None, f"Starting location not found: {start}"

    # Check whether the destination exists.
    if destination not in campus_graph:
        return None, f"Destination not found: {destination}"

    # If start and destination are the same.
    if start == destination:
        return [start], None

    # Store distances from the starting location.
    distances = {
        location: float("inf")
        for location in campus_graph
    }

    # Store the previous location in the shortest route.
    previous = {
        location: None
        for location in campus_graph
    }

    distances[start] = 0

    # Priority queue: (distance, location)
    priority_queue = [(0, start)]

    while priority_queue:

        current_distance, current_location = heapq.heappop(
            priority_queue
        )

        # Ignore outdated queue entries.
        if current_distance > distances[current_location]:
            continue

        # Stop when the destination is reached.
        if current_location == destination:
            break

        # Explore connected locations.
        for neighbour, weight in campus_graph[
            current_location
        ].items():

            new_distance = current_distance + weight

            if new_distance < distances[neighbour]:

                distances[neighbour] = new_distance

                previous[neighbour] = current_location

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbour)
                )

    # Check whether the destination was reached.
    if distances[destination] == float("inf"):
        return None, "No route found between these locations."

    # Reconstruct the route.
    path = []
    current_location = destination

    while current_location is not None:
        path.append(current_location)
        current_location = previous[current_location]

    # Reverse the route to get start -> destination.
    path.reverse()

    return path, None


# ============================================================
# TEST THE ALGORITHM
# ============================================================

if __name__ == "__main__":

    print("=" * 55)
    print("       NCERC SHORTEST PATH TEST")
    print("=" * 55)

    start = "Main Gate"

    destination = "Room 226 - Advanced Computing Lab"

    path, error = find_shortest_path(
        start,
        destination
    )

    if error:
        print("\nError:", error)

    else:
        print("\nStarting Location:", start)

        print("Destination:", destination)

        print("\nSuggested Route:")

        for step_number, location in enumerate(path, start=1):
            print(f"{step_number}. {location}")

        print("\nTotal logical transitions:", len(path) - 1)