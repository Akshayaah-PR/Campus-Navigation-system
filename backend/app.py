# NCERC CAMPUS NAVIGATION SYSTEM
# Flask Backend

from flask import Flask, request, jsonify
from flask_cors import CORS

from graph import campus_graph, locations
from algorithm import find_shortest_path


app = Flask(__name__)
CORS(app)


# ============================================================
# DEPARTMENT INFORMATION
# ============================================================

DEPARTMENT_CORRIDORS = {
    "First Floor - Artificial Intelligence Corridor":
        "Artificial Intelligence",

    "First Floor - Mechanical Engineering Corridor":
        "Mechanical Engineering",

    "Second Floor - Computer Science and Engineering Corridor":
        "Computer Science and Engineering",

    "Second Floor - Electrical and Electronics Engineering Corridor":
        "Electrical and Electronics Engineering",

    "Third Floor - Electronics and Communication Engineering Corridor":
        "Electronics and Communication Engineering",

    "Third Floor - Mechatronics Engineering Corridor":
        "Mechatronics Engineering"
}


# ============================================================
# GET THE DEPARTMENT OF A LOCATION
# ============================================================

def get_department(location_id):
    """
    Identify the department from the location's connected
    department corridor.

    This uses the existing campus graph.
    """

    # If the location itself is a department corridor
    if location_id in DEPARTMENT_CORRIDORS:
        return DEPARTMENT_CORRIDORS[location_id]

    # Check the location's connected neighbours
    neighbours = campus_graph.get(location_id, {})

    for neighbour in neighbours:

        if neighbour in DEPARTMENT_CORRIDORS:
            return DEPARTMENT_CORRIDORS[neighbour]

    # No department has been assigned or identified
    return ""


# ============================================================
# GENERATE STEP-BY-STEP INSTRUCTIONS
# ============================================================

def create_instruction(location_id, index, total_steps, destination):
    """
    Generate a simple instruction for each location in the route.

    These are logical directions based on graph connections,
    not GPS-based or verified turn-by-turn directions.
    """

    details = locations.get(location_id, {})

    name = details.get("name", location_id)
    floor = details.get("floor", "")
    category = details.get("category", "")

    # First step
    if index == 0:
        return f"Start at {name}."

    # Final step
    if index == total_steps - 1:
        return f"You have reached your destination: {name}."

    # Staircase instructions
    if category == "Staircase":
        return (
            "Use the central staircase to reach the floor "
            "containing your destination."
        )

    # Floor landing instructions
    if category == "Floor Landing":
        return (
            f"Reach the {floor} landing and continue "
            "towards the appropriate corridor."
        )

    # Corridor instructions
    if category in ["Corridor", "Department Corridor"]:

        department = get_department(location_id)

        if department:
            return (
                f"Follow the {department} corridor "
                f"towards {destination}."
            )

        return (
            f"Follow the corridor towards {destination}."
        )

    # Department and classroom information
    department = get_department(location_id)

    if category == "Classroom" and department:
        return (
            f"Proceed to {name} in the {department} "
            f"department, {floor}."
        )

    # General location instruction
    if floor:
        return f"Proceed to {name} on the {floor}."

    return f"Proceed to {name}."


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return jsonify({
        "message": "Welcome to NCERC Campus Navigation System",
        "status": "Backend is running"
    })


# ============================================================
# GET ALL CAMPUS LOCATIONS
# ============================================================

@app.route("/locations", methods=["GET"])
def get_locations():

    location_list = []

    for location_id in campus_graph.keys():

        details = locations.get(location_id, {})

        location_list.append({
            "id": location_id,
            "name": details.get("name") or location_id,
            "floor": details.get("floor") or "",
            "category": details.get("category") or "",
            "department": get_department(location_id),
            "note": details.get("note") or ""
        })

    return jsonify({
        "total_locations": len(location_list),
        "locations": location_list
    })


# ============================================================
# SEARCH CAMPUS LOCATIONS
# ============================================================

@app.route("/search", methods=["GET"])
def search_locations():

    query = request.args.get("q", "").strip().lower()

    if not query:
        return jsonify({"results": []})

    results = []

    for location_id in campus_graph.keys():

        details = locations.get(location_id, {})

        name = str(details.get("name") or location_id)
        floor = str(details.get("floor") or "")
        category = str(details.get("category") or "")
        note = str(details.get("note") or "")

        aliases = details.get("aliases") or []

        if isinstance(aliases, str):
            aliases = [aliases]

        aliases = [
            str(alias)
            for alias in aliases
            if alias is not None
        ]

        department = get_department(location_id)

        searchable_text = " ".join([
            location_id,
            name,
            floor,
            category,
            note,
            department,
            " ".join(aliases)
        ]).lower()

        if query in searchable_text:

            results.append({
                "id": location_id,
                "name": name,
                "floor": floor,
                "category": category,
                "department": department
            })

    return jsonify({
        "query": query,
        "results": results
    })


# ============================================================
# FIND THE SHORTEST ROUTE
# ============================================================

@app.route("/find-route", methods=["GET"])
def find_route():

    start = request.args.get("start", "").strip()
    destination = request.args.get("destination", "").strip()

    if not start or not destination:

        return jsonify({
            "error": (
                "Please provide both a starting location "
                "and destination."
            )
        }), 400

    path, error = find_shortest_path(start, destination)

    if error:

        return jsonify({
            "error": error
        }), 400

    route_steps = []

    total_steps = len(path)

    for index, location_id in enumerate(path):

        details = locations.get(location_id, {})

        name = details.get("name") or location_id
        floor = details.get("floor") or ""
        category = details.get("category") or ""
        department = get_department(location_id)
        note = details.get("note") or ""

        instruction = create_instruction(
            location_id,
            index,
            total_steps,
            destination
        )

        route_steps.append({
            "step": index + 1,
            "id": location_id,
            "name": name,
            "floor": floor,
            "category": category,
            "department": department,
            "note": note,
            "instruction": instruction
        })

    return jsonify({
        "start": start,
        "destination": destination,
        "route": path,
        "route_steps": route_steps,
        "total_transitions": len(path) - 1,
        "message": "Shortest route found successfully.",
        "route_type": "Logical campus graph route"
    })


# ============================================================
# START THE SERVER
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)