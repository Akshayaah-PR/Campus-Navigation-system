"""
NCERC CAMPUS NAVIGATION SYSTEM
--------------------------------
This file contains:
1. Campus locations
2. Location details for searching
3. Connections between locations
4. A graph for the shortest-path algorithm

IMPORTANT:
- Edge weights represent logical transitions, not metres.
- Outdoor connections are provisional and need verification.
- Indoor room connections are logical placeholders, not verified
  room-by-room walking paths.
"""

# ============================================================
# 1. LOCATION DATABASE
# ============================================================

locations = {}


def add_location(
    name,
    floor=None,
    category="Location",
    aliases=None,
    note=""
):
    """Add a location and its searchable information."""

    locations[name] = {
        "name": name,
        "floor": floor,
        "category": category,
        "aliases": aliases or [],
        "note": note
    }


# ============================================================
# 2. CAMPUS OUTDOOR LOCATIONS
# ============================================================

add_location(
    "Main Gate",
    category="Entrance",
    aliases=["gate", "main entrance", "college entrance"]
)

add_location(
    "Bhaskara Block",
    category="Building",
    aliases=["bhaskara", "bhaskara building"]
)


add_location(
    "Nala Canteen",
    category="Food",
    aliases=["canteen", "nala", "food"]
)

add_location(
    "Aryabhatta Block",
    category="Building",
    aliases=["aryabhatta", "aryabhatta building"]
)


# ============================================================
# 3. FLOOR LANDINGS
# ============================================================

floor_names = {
    0: "Ground Floor",
    1: "First Floor",
    2: "Second Floor",
    3: "Third Floor",
    4: "Fourth Floor"
}

landing_names = {}

for floor_number, floor_name in floor_names.items():

    if floor_number == 0:
        landing = "Aryabhatta - Ground Floor Landing"
    else:
        landing = f"Aryabhatta - {floor_number}{'st' if floor_number == 1 else 'nd' if floor_number == 2 else 'rd' if floor_number == 3 else 'th'} Floor Landing"

    landing_names[floor_number] = landing

    add_location(
        landing,
        floor=floor_name,
        category="Floor Landing",
        aliases=[
            floor_name,
            f"{floor_name} landing"
        ],
        note="Use the central staircase to reach this floor."
    )


add_location(
    "Aryabhatta Central Staircase",
    category="Staircase",
    aliases=[
        "central staircase",
        "stairs",
        "staircase"
    ],
    note="The central staircase connects all floors."
)


# ============================================================
# 4. GROUND FLOOR
# ============================================================

ground_floor_locations = [
    ("Room 101", "Classroom"),
    ("Room 102", "Classroom"),
    ("Room 103", "Classroom"),

    ("Room 105 - Internet Technologies Lab", "Laboratory"),
    ("Room 106 - Advanced Simulation Lab", "Laboratory"),

    ("Students' Toilet - Ground Floor", "Restroom"),
    ("Ladies' Students' Toilet - Ground Floor", "Restroom"),

    ("Room 110 - CASIT Lab", "Laboratory"),
    ("Room 111 - Advanced Software Lab", "Laboratory"),

    ("Staff Toilet - Ground Floor", "Restroom"),

    ("Room 113", "Classroom"),
    ("Room 114", "Classroom"),
    ("Room 115", "Classroom")
]

for name, category in ground_floor_locations:
    add_location(
        name,
        floor="Ground Floor",
        category=category
    )


add_location(
    "Ground Floor - Rooms 101 to 106 Corridor",
    floor="Ground Floor",
    category="Corridor",
    aliases=["ground floor corridor 1"],
    note="Follow room-number signage to find the destination."
)

add_location(
    "Ground Floor - Rooms 110 to 115 Corridor",
    floor="Ground Floor",
    category="Corridor",
    aliases=["ground floor corridor 2"],
    note="Follow room-number signage to find the destination."
)


# ============================================================
# 5. FIRST FLOOR
# ============================================================

first_floor_locations = [
    ("Principal's Office", "Office"),
    ("Academic Office", "Office"),

    ("Room 201", "Classroom"),
    ("Room 202", "Classroom"),
    ("Room 203", "Classroom"),

    ("Room 205 - Mechanical Faculty Cabin", "Faculty Cabin"),
    ("Room 206 - Mechanical Faculty Cabin", "Faculty Cabin"),
    ("Room 207 - Mechanical Faculty Cabin", "Faculty Cabin"),
    ("Room 208 - Mechanical Faculty Cabin", "Faculty Cabin"),
    ("Room 209 - Mechanical Faculty Cabin", "Faculty Cabin"),
    ("Room 210 - Mechanical Faculty Cabin", "Faculty Cabin"),
    ("Room 211 - Mechanical Faculty Cabin", "Faculty Cabin"),
    ("Room 212 - Mechanical Faculty Cabin", "Faculty Cabin"),
    ("Room 213 - Mechanical Faculty Cabin", "Faculty Cabin"),
    ("Room 214 - Mechanical Faculty Cabin", "Faculty Cabin"),

    ("Room 216", "Classroom"),
    ("Room 218", "Classroom"),

    ("Room 221 - AI Faculty Cabin", "Faculty Cabin"),
    ("Room 222 - AI Faculty Cabin", "Faculty Cabin"),
    ("Room 223 - AI Faculty Cabin", "Faculty Cabin"),
    ("Room 224 - AI Faculty Cabin", "Faculty Cabin"),
    ("Room 225 - AI Faculty Cabin", "Faculty Cabin"),

    ("Room 226 - Advanced Computing Lab", "Laboratory"),
    ("Room 227 - Advanced CAD/CAM Lab", "Laboratory"),

    ("Room 228", "Classroom"),
    ("Room 229", "Classroom"),

    ("Ladies' Students' Toilet - First Floor", "Restroom"),
    ("Ladies' Staff Toilet - First Floor", "Restroom"),

    ("Gents' Students' Toilet - First Floor", "Restroom"),
    ("Gents' Staff Toilet - First Floor", "Restroom")
]

for name, category in first_floor_locations:
    add_location(
        name,
        floor="First Floor",
        category=category
    )


add_location(
    "First Floor - Artificial Intelligence Corridor",
    floor="First Floor",
    category="Department Corridor",
    aliases=["AI", "AI department", "artificial intelligence"],
    note="Follow the Artificial Intelligence department sign."
)

add_location(
    "First Floor - Mechanical Engineering Corridor",
    floor="First Floor",
    category="Department Corridor",
    aliases=["mechanical", "mechanical engineering"],
    note="Follow the Mechanical Engineering department sign."
)


# ============================================================
# 6. SECOND FLOOR
# ============================================================

second_floor_locations = [
    ("IQAC Office", "Office"),
    ("Director's Office", "Office"),
    ("IQAC Conference Room", "Conference Room"),
    ("M.Tech Classroom - Second Floor", "Classroom"),

    ("Room 301", "Classroom"),
    ("Room 302", "Classroom"),
    ("Room 303", "Classroom"),

    ("Room 305 - EEE Faculty Cabin", "Faculty Cabin"),
    ("Room 306 - EEE Faculty Cabin", "Faculty Cabin"),
    ("Room 307 - EEE Faculty Cabin", "Faculty Cabin"),
    ("Room 308 - EEE Faculty Cabin", "Faculty Cabin"),
    ("Room 309 - EEE Faculty Cabin", "Faculty Cabin"),
    ("Room 310 - EEE Faculty Cabin", "Faculty Cabin"),
    ("Room 311 - EEE Faculty Cabin", "Faculty Cabin"),
    ("Room 312 - EEE Faculty Cabin", "Faculty Cabin"),
    ("Room 313 - EEE Faculty Cabin", "Faculty Cabin"),
    ("Room 314 - EEE Faculty Cabin", "Faculty Cabin"),

    ("Room 316", "Classroom"),
    ("Room 318", "Classroom"),

    ("Room 320 - CSE Faculty Cabin", "Faculty Cabin"),
    ("Room 321 - CSE Faculty Cabin", "Faculty Cabin"),
    ("Room 322 - CSE Faculty Cabin", "Faculty Cabin"),
    ("Room 323 - CSE Faculty Cabin", "Faculty Cabin"),
    ("Room 324 - CSE Faculty Cabin", "Faculty Cabin"),
    ("Room 325 - CSE Faculty Cabin", "Faculty Cabin"),
    ("Room 326 - CSE Faculty Cabin", "Faculty Cabin"),
    ("Room 327 - CSE Faculty Cabin", "Faculty Cabin"),
    ("Room 328 - CSE Faculty Cabin", "Faculty Cabin"),
    ("Room 329 - CSE Faculty Cabin", "Faculty Cabin"),

    ("Room 331", "Classroom"),
    ("Room 332", "Classroom"),
    ("Room 333", "Classroom"),

    ("Ladies' Students' Toilet - Second Floor", "Restroom"),
    ("Ladies' Staff Toilet - Second Floor", "Restroom"),

    ("Gents' Students' Toilet - Second Floor", "Restroom"),
    ("Gents' Staff Toilet - Second Floor", "Restroom")
]

for name, category in second_floor_locations:
    add_location(
        name,
        floor="Second Floor",
        category=category
    )


add_location(
    "Second Floor - Computer Science and Engineering Corridor",
    floor="Second Floor",
    category="Department Corridor",
    aliases=["CSE", "computer science", "CSE department"],
    note="Follow the Computer Science and Engineering department sign."
)

add_location(
    "Second Floor - Electrical and Electronics Engineering Corridor",
    floor="Second Floor",
    category="Department Corridor",
    aliases=["EEE", "electrical engineering", "EEE department"],
    note="Follow the Electrical and Electronics Engineering department sign."
)


# ============================================================
# 7. THIRD FLOOR
# ============================================================

third_floor_locations = [
    ("Board Room", "Meeting Room"),
    ("NCPIR Office", "Office"),

    ("Room 401", "Classroom"),
    ("Room 402", "Classroom"),
    ("Room 403", "Classroom"),

    ("Room 405 - Mechatronics Faculty Cabin", "Faculty Cabin"),
    ("Room 406 - Mechatronics Faculty Cabin", "Faculty Cabin"),
    ("Room 407 - Mechatronics Faculty Cabin", "Faculty Cabin"),
    ("Room 408 - Mechatronics Faculty Cabin", "Faculty Cabin"),
    ("Room 409 - Mechatronics Faculty Cabin", "Faculty Cabin"),
    ("Room 410 - Mechatronics Faculty Cabin", "Faculty Cabin"),
    ("Room 411 - Mechatronics Faculty Cabin", "Faculty Cabin"),
    ("Room 412 - Mechatronics Faculty Cabin", "Faculty Cabin"),
    ("Room 413 - Mechatronics Faculty Cabin", "Faculty Cabin"),
    ("Room 414 - Mechatronics Faculty Cabin", "Faculty Cabin"),

    ("Room 416", "Classroom"),
    ("Room 418", "Classroom"),

    ("Room 420 - ECE Faculty Cabin", "Faculty Cabin"),
    ("Room 421 - ECE Faculty Cabin", "Faculty Cabin"),
    ("Room 422 - ECE Faculty Cabin", "Faculty Cabin"),
    ("Room 423 - ECE Faculty Cabin", "Faculty Cabin"),
    ("Room 424 - ECE Faculty Cabin", "Faculty Cabin"),
    ("Room 425 - ECE Faculty Cabin", "Faculty Cabin"),
    ("Room 426 - ECE Faculty Cabin", "Faculty Cabin"),
    ("Room 427 - ECE Faculty Cabin", "Faculty Cabin"),
    ("Room 428 - ECE Faculty Cabin", "Faculty Cabin"),
    ("Room 429 - ECE Faculty Cabin", "Faculty Cabin"),

    ("Room 433", "Classroom"),
    ("Room 434", "Classroom"),
    ("Room 435", "Classroom"),

    ("Ladies' Students' Toilet - Third Floor", "Restroom"),
    ("Ladies' Staff Toilet - Third Floor", "Restroom"),

    ("Gents' Students' Toilet - Third Floor", "Restroom"),
    ("Gents' Staff Toilet - Third Floor", "Restroom")
]

for name, category in third_floor_locations:
    add_location(
        name,
        floor="Third Floor",
        category=category
    )


add_location(
    "Third Floor - Electronics and Communication Engineering Corridor",
    floor="Third Floor",
    category="Department Corridor",
    aliases=["ECE", "electronics and communication", "ECE department"],
    note="Follow the Electronics and Communication Engineering department sign."
)

add_location(
    "Third Floor - Mechatronics Engineering Corridor",
    floor="Third Floor",
    category="Department Corridor",
    aliases=["MTR", "mechatronics", "mechatronics engineering"],
    note="Follow the Mechatronics Engineering department sign."
)


# ============================================================
# 8. FOURTH FLOOR
# ============================================================

fourth_floor_locations = [
    ("Dining Room", "Dining Room"),
    ("Room 501 - Main Seminar Hall", "Seminar Hall"),
    ("Room 504 - Classroom", "Classroom"),
    ("Room 505 - M.Tech Classroom", "Classroom"),
    ("Room 505A - M.Tech Classroom", "Classroom"),
    ("Room 506 - Classroom", "Classroom"),
    ("Room 509 - Classroom", "Classroom"),
    ("Room 510 - Seminar Hall", "Seminar Hall"),

    ("Cyber Security Lab", "Laboratory"),
    ("Research Lab 1 - Room Number Unconfirmed", "Laboratory"),
    ("Research Lab 2 - Room Number Unconfirmed", "Laboratory"),
    ("VLSI and Embedded Lab", "Laboratory")
]

for name, category in fourth_floor_locations:
    add_location(
        name,
        floor="Fourth Floor",
        category=category,
        note="Follow the destination signs on this floor."
    )


add_location(
    "Fourth Floor - General Corridor",
    floor="Fourth Floor",
    category="Corridor",
    aliases=["fourth floor corridor"],
    note="Follow room-number and destination signs."
)


# ============================================================
# 9. BUILD THE CAMPUS GRAPH
# ============================================================

# Each location starts with an empty list of connections.

campus_graph = {
    location_name: {}
    for location_name in locations
}


def connect_locations(location_a, location_b, weight=1):
    """
    Connect two existing locations in both directions.

    Weight represents a logical transition, not a measured distance.
    """

    if location_a not in campus_graph:
        raise ValueError(f"Location not found: {location_a}")

    if location_b not in campus_graph:
        raise ValueError(f"Location not found: {location_b}")

    campus_graph[location_a][location_b] = weight
    campus_graph[location_b][location_a] = weight


# ------------------------------------------------------------
# 9A. Outdoor connections (provisional)
# ------------------------------------------------------------

# Verify these connections at the actual campus before relying on them.

connect_locations("Main Gate", "Bhaskara Block")
connect_locations("Bhaskara Block", "Aryabhatta Block")
connect_locations("Main Gate", "Nala Canteen")


# ------------------------------------------------------------
# 9B. Central staircase and floor landings
# ------------------------------------------------------------

for floor_number in range(5):
    landing = landing_names[floor_number]

    connect_locations("Aryabhatta Block", landing)
    connect_locations(landing, "Aryabhatta Central Staircase")


# ------------------------------------------------------------
# 9C. Ground-floor corridors
# ------------------------------------------------------------

ground_corridor_1 = "Ground Floor - Rooms 101 to 106 Corridor"
ground_corridor_2 = "Ground Floor - Rooms 110 to 115 Corridor"

connect_locations(landing_names[0], ground_corridor_1)
connect_locations(landing_names[0], ground_corridor_2)

for name, category in ground_floor_locations:

    if name in [
        "Room 101",
        "Room 102",
        "Room 103",
        "Room 105 - Internet Technologies Lab",
        "Room 106 - Advanced Simulation Lab",
        "Students' Toilet - Ground Floor",
        "Ladies' Students' Toilet - Ground Floor"
    ]:
        connect_locations(ground_corridor_1, name)

    else:
        connect_locations(ground_corridor_2, name)


# ------------------------------------------------------------
# 9D. First-floor corridors
# ------------------------------------------------------------

ai_corridor = "First Floor - Artificial Intelligence Corridor"
mechanical_corridor = "First Floor - Mechanical Engineering Corridor"

connect_locations(landing_names[1], ai_corridor)
connect_locations(landing_names[1], mechanical_corridor)

for name, category in first_floor_locations:

    if (
        "AI Faculty Cabin" in name
        or name in [
            "Room 218",
            "Room 228",
            "Room 229",
            "Room 226 - Advanced Computing Lab",
            "Room 227 - Advanced CAD/CAM Lab",
            "Ladies' Students' Toilet - First Floor",
            "Ladies' Staff Toilet - First Floor"
        ]
    ):
        connect_locations(ai_corridor, name)

    elif (
        "Mechanical Faculty Cabin" in name
        or name in [
            "Room 201",
            "Room 202",
            "Room 203",
            "Room 216",
            "Gents' Students' Toilet - First Floor",
            "Gents' Staff Toilet - First Floor"
        ]
    ):
        connect_locations(mechanical_corridor, name)

    else:
        # Offices and other unspecified destinations are linked
        # to the landing until their precise corridor is verified.
        connect_locations(landing_names[1], name)


# ------------------------------------------------------------
# 9E. Second-floor corridors
# ------------------------------------------------------------

cse_corridor = (
    "Second Floor - Computer Science and Engineering Corridor"
)

eee_corridor = (
    "Second Floor - Electrical and Electronics Engineering Corridor"
)

connect_locations(landing_names[2], cse_corridor)
connect_locations(landing_names[2], eee_corridor)

for name, category in second_floor_locations:

    if (
        "CSE Faculty Cabin" in name
        or name in [
            "Room 318",
            "Room 331",
            "Room 332",
            "Room 333",
            "Ladies' Students' Toilet - Second Floor",
            "Ladies' Staff Toilet - Second Floor"
        ]
    ):
        connect_locations(cse_corridor, name)

    elif (
        "EEE Faculty Cabin" in name
        or name in [
            "Room 301",
            "Room 302",
            "Room 303",
            "Room 316",
            "Gents' Students' Toilet - Second Floor",
            "Gents' Staff Toilet - Second Floor"
        ]
    ):
        connect_locations(eee_corridor, name)

    else:
        connect_locations(landing_names[2], name)


# ------------------------------------------------------------
# 9F. Third-floor corridors
# ------------------------------------------------------------

ece_corridor = (
    "Third Floor - Electronics and Communication Engineering Corridor"
)

mechatronics_corridor = (
    "Third Floor - Mechatronics Engineering Corridor"
)

connect_locations(landing_names[3], ece_corridor)
connect_locations(landing_names[3], mechatronics_corridor)

for name, category in third_floor_locations:

    if (
        "ECE Faculty Cabin" in name
        or name in [
            "Room 418",
            "Room 433",
            "Room 434",
            "Room 435",
            "Ladies' Students' Toilet - Third Floor",
            "Ladies' Staff Toilet - Third Floor"
        ]
    ):
        connect_locations(ece_corridor, name)

    elif (
        "Mechatronics Faculty Cabin" in name
        or name in [
            "Room 401",
            "Room 402",
            "Room 403",
            "Room 416",
            "Gents' Students' Toilet - Third Floor",
            "Gents' Staff Toilet - Third Floor"
        ]
    ):
        connect_locations(mechatronics_corridor, name)

    else:
        connect_locations(landing_names[3], name)


# ------------------------------------------------------------
# 9G. Fourth-floor destinations
# ------------------------------------------------------------

fourth_corridor = "Fourth Floor - General Corridor"

connect_locations(landing_names[4], fourth_corridor)

for name, category in fourth_floor_locations:
    connect_locations(fourth_corridor, name)


# ============================================================
# 10. GRAPH VALIDATION
# ============================================================

def validate_graph():
    """Check that all connections point to existing locations."""

    for location_name, connections in campus_graph.items():

        for neighbour in connections:

            if neighbour not in campus_graph:
                return False, (
                    f"{location_name} connects to missing location "
                    f"{neighbour}"
                )

            if location_name not in campus_graph[neighbour]:
                return False, (
                    f"Connection between {location_name} and "
                    f"{neighbour} is not bidirectional"
                )

    return True, "All graph connections are valid."


# ============================================================
# 11. TEST THE GRAPH
# ============================================================

if __name__ == "__main__":

    print("=" * 55)
    print("       NCERC CAMPUS NAVIGATION SYSTEM")
    print("=" * 55)

    print(f"\nTotal locations: {len(locations)}")
    print(f"Total graph nodes: {len(campus_graph)}")

    valid, message = validate_graph()

    print("\nGraph validation:")
    print(message)

    print("\nSample locations:")

    for location_name in list(locations.keys())[:10]:
        print("-", location_name)

    if valid:
        print("\nGraph loaded successfully!")
    else:
        print("\nPlease fix the graph connections before continuing.")