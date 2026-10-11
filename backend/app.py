# NCERC CAMPUS NAVIGATION SYSTEM
# Flask Backend

from flask import Flask, request, jsonify
from flask_cors import CORS

from graph import campus_graph, locations
from algorithm import find_shortest_path

# Create the Flask application
app = Flask(__name__)

# Allow communication with the frontend
CORS(app)


# HOME PAGE / BACKEND STATUS
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to NCERC Campus Navigation System",
        "status": "Backend is running"
    })


# GET ALL CAMPUS LOCATIONS
@app.route("/locations", methods=["GET"])
def get_locations():

    location_list = []

    for location_id in campus_graph.keys():

        details = locations.get(location_id, {})

        location_list.append({
            "id": location_id,
            "name": str(details.get("name") or location_id),
            "floor": str(details.get("floor") or ""),
            "category": str(details.get("category") or ""),
            "note": str(details.get("note") or "")
        })

    return jsonify({
        "total_locations": len(location_list),
        "locations": location_list
    })


# SEARCH CAMPUS LOCATIONS
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

        # Ensure aliases are strings
        if isinstance(aliases, str):
            aliases = [aliases]

        aliases = [
            str(alias)
            for alias in aliases
            if alias is not None
        ]

        searchable_text = " ".join([
            str(location_id),
            name,
            floor,
            category,
            note,
            " ".join(aliases)
        ]).lower()

        if query in searchable_text:

            results.append({
                "id": location_id,
                "name": name,
                "floor": floor,
                "category": category
            })

    return jsonify({
        "query": query,
        "results": results
    })


# FIND THE SHORTEST ROUTE
@app.route("/find-route", methods=["GET"])
def find_route():

    start = request.args.get("start", "").strip()
    destination = request.args.get("destination", "").strip()

    if not start or not destination:
        return jsonify({
            "error": "Please provide both a starting location and destination."
        }), 400

    path, error = find_shortest_path(start, destination)

    if error:
        return jsonify({
            "error": error
        }), 400

    route_steps = []

    for index, location_id in enumerate(path, start=1):

        details = locations.get(location_id, {})

        route_steps.append({
            "step": index,
            "id": location_id,
            "name": str(details.get("name") or location_id),
            "floor": str(details.get("floor") or ""),
            "category": str(details.get("category") or ""),
            "note": str(details.get("note") or "")
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


# START THE SERVER
if __name__ == "__main__":
    app.run(debug=True)