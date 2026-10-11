const API_URL = "http://127.0.0.1:5000";

// Get HTML elements
const startSelect = document.getElementById("start");
const destinationSelect = document.getElementById("destination");
const findRouteButton = document.getElementById("findRoute");
const swapButton = document.getElementById("swapLocations");
const message = document.getElementById("message");
const routeResult = document.getElementById("routeResult");

const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");
const searchMessage = document.getElementById("searchMessage");
const searchResults = document.getElementById("searchResults");

// Load all campus locations
async function loadLocations() {
try {
const response = await fetch(`${API_URL}/locations`);

```
    if (!response.ok) {
        throw new Error("Could not get campus locations.");
    }

    const data = await response.json();

    // Backend returns an object containing a locations array
    const locations = data.locations;

    if (!Array.isArray(locations)) {
        throw new Error("The locations data format is incorrect.");
    }

    // Clear old options
    startSelect.innerHTML = '<option value="">Select starting location</option>';
    destinationSelect.innerHTML = '<option value="">Select destination</option>';

    // Add locations to both dropdowns
    locations.forEach(function (location) {
        const option1 = document.createElement("option");
        option1.value = location.id;
        option1.textContent = location.name;
        startSelect.appendChild(option1);

        const option2 = document.createElement("option");
        option2.value = location.id;
        option2.textContent = location.name;
        destinationSelect.appendChild(option2);
    });

    console.log("Campus locations loaded:", locations.length);

} catch (error) {
    console.error("Location loading error:", error);

    startSelect.innerHTML = '<option value="">Failed to load locations</option>';
    destinationSelect.innerHTML = '<option value="">Failed to load locations</option>';

    message.textContent =
        "Could not load locations. Check whether the backend is running.";
}
```

}

// Find the shortest route
async function findRoute() {
const start = startSelect.value;
const destination = destinationSelect.value;

```
message.textContent = "";
routeResult.innerHTML = "";

if (!start || !destination) {
    message.textContent = "Please select both starting location and destination.";
    return;
}

if (start === destination) {
    message.textContent = "Starting location and destination must be different.";
    return;
}

try {
    const url =
        `${API_URL}/find-route?start=${encodeURIComponent(start)}` +
        `&destination=${encodeURIComponent(destination)}`;

    const response = await fetch(url);
    const data = await response.json();

    if (!response.ok || data.error) {
        throw new Error(data.error || "Could not find a route.");
    }

    const heading = document.createElement("h3");
    heading.textContent = "Your Route";
    routeResult.appendChild(heading);

    const list = document.createElement("ol");

    // Prefer route_steps when the backend provides them
    if (Array.isArray(data.route_steps) && data.route_steps.length > 0) {
        data.route_steps.forEach(function (step) {
            const item = document.createElement("li");

            const name =
                typeof step === "string"
                    ? step
                    : (step.name || step.id || "Campus location");

            item.textContent = name;

            if (typeof step === "object" && step.floor) {
                item.textContent += ` — ${step.floor}`;
            }

            list.appendChild(item);
        });
    } else if (Array.isArray(data.route)) {
        data.route.forEach(function (location) {
            const item = document.createElement("li");
            item.textContent =
                typeof location === "string"
                    ? location
                    : (location.name || location.id || "Campus location");

            list.appendChild(item);
        });
    } else {
        throw new Error("The backend returned an unexpected route format.");
    }

    routeResult.appendChild(list);

    if (data.total_transitions !== undefined) {
        const total = document.createElement("p");
        total.textContent = `Total transitions: ${data.total_transitions}`;
        routeResult.appendChild(total);
    }

} catch (error) {
    console.error("Route error:", error);
    message.textContent = error.message || "Something went wrong while finding the route.";
}
```

}

// Search for a campus location
async function searchLocations(event) {
if (event) {
event.preventDefault();
}

```
const query = searchInput.value.trim();

searchResults.innerHTML = "";
searchMessage.textContent = "";

if (!query) {
    searchMessage.textContent = "Please enter a location to search.";
    return;
}

try {
    const response = await fetch(
        `${API_URL}/search?q=${encodeURIComponent(query)}`
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Search failed.");
    }

    const results = data.results || [];

    if (results.length === 0) {
        searchMessage.textContent = "No matching locations found.";
        return;
    }

    results.forEach(function (location) {
        const item = document.createElement("div");
        item.className = "search-result-item";

        const name = document.createElement("strong");
        name.textContent = location.name;
        item.appendChild(name);

        if (location.floor) {
            const floor = document.createElement("p");
            floor.textContent = location.floor;
            item.appendChild(floor);
        }

        item.addEventListener("click", function () {
            startSelect.value = location.id;
            searchMessage.textContent =
                `Selected ${location.name} as the starting location.`;

            destinationSelect.focus();
        });

        searchResults.appendChild(item);
    });

} catch (error) {
    console.error("Search error:", error);
    searchMessage.textContent =
        "Search failed. Please check the backend and try again.";
}
```

}

// Swap the starting point and destination
function swapLocations() {
const startValue = startSelect.value;
const destinationValue = destinationSelect.value;

```
startSelect.value = destinationValue;
destinationSelect.value = startValue;
```

}

// Connect buttons a
