// ================================================
// 1. BACKEND CONNECTION
// ================================================

const API_URL = "http://127.0.0.1:5000";

// ================================================
// 2. GET HTML ELEMENTS
// ================================================

const startSelect = document.getElementById("start");

const destinationSelect = document.getElementById("destination");

const findRouteButton = document.getElementById("findRoute");

const swapLocationsButton = document.getElementById("swapLocations");

const message = document.getElementById("message");

const routeResult = document.getElementById("routeResult");

const searchForm = document.getElementById("searchForm");

const searchInput = document.getElementById("searchInput");

const searchButton = document.getElementById("searchButton");

const searchMessage = document.getElementById("searchMessage");

const searchResults = document.getElementById("searchResults");

// Store all campus locations here.
let campusLocations = [];

// ================================================
// 3. DISPLAY STATUS MESSAGES
// ================================================

function showMessage(text, type = "") {

```
message.textContent = text;

message.className = type;
```

}

function showSearchMessage(text) {

```
searchMessage.textContent = text;
```

}

// ================================================
// 4. LOAD CAMPUS LOCATIONS
// ================================================

async function loadLocations() {

```
showMessage("Loading campus locations...");

try {

    const response = await fetch(`${API_URL}/locations`);

    if (!response.ok) {

        throw new Error("Unable to load campus locations.");

    }

    const data = await response.json();

    // Save the returned location objects.
    campusLocations = data.locations || [];

    // Clear old dropdown options.
    startSelect.innerHTML = "";

    destinationSelect.innerHTML = "";


    // Add default options.
    const startDefault = document.createElement("option");

    startDefault.value = "";

    startDefault.textContent = "Select starting location";

    startSelect.appendChild(startDefault);


    const destinationDefault = document.createElement("option");

    destinationDefault.value = "";

    destinationDefault.textContent = "Select destination";

    destinationSelect.appendChild(destinationDefault);


    // Add every location to both dropdowns.
    campusLocations.forEach(location => {

        const startOption = document.createElement("option");

        startOption.value = location.id;

        startOption.textContent = location.name;

        startSelect.appendChild(startOption);


        const destinationOption = document.createElement("option");

        destinationOption.value = location.id;

        destinationOption.textContent = location.name;

        destinationSelect.appendChild(destinationOption);

    });


    showMessage(
        `${campusLocations.length} campus locations loaded successfully.`,
        "success"
    );

} catch (error) {

    console.error("Location loading error:", error);

    showMessage(
        "Could not connect to Flask. Please start the backend and try again.",
        "error"
    );

    startSelect.innerHTML =
        '<option value="">Backend unavailable</option>';

    destinationSelect.innerHTML =
        '<option value="">Backend unavailable</option>';

}
```

}

// ================================================
// 5. FIND SHORTEST ROUTE
// ================================================

async function findRoute() {

```
const start = startSelect.value;

const destination = destinationSelect.value;


// Clear previous results.
routeResult.innerHTML = "";


// Validate the selections.
if (!start || !destination) {

    showMessage(
        "Please select both a starting location and a destination.",
        "error"
    );

    return;

}


if (start === destination) {

    showMessage(
        "Your starting location and destination are the same.",
        "error"
    );

    return;

}


// Show loading status.
showMessage("Calculating the shortest route...");

findRouteButton.disabled = true;


try {

    const url =
        `${API_URL}/find-route?start=${encodeURIComponent(start)}` +
        `&destination=${encodeURIComponent(destination)}`;


    const response = await fetch(url);

    const data = await response.json();


    if (!response.ok) {

        throw new Error(data.error || "Unable to find a route.");

    }


    // Display success message.
    showMessage(
        "Shortest route found successfully!",
        "success"
    );


    // Build the route summary.
    const summary = document.createElement("div");

    summary.className = "route-summary";


    const summaryTitle = document.createElement("h3");

    summaryTitle.textContent = "Your Route is Ready!";


    const startText = document.createElement("p");

    startText.textContent = `From: ${getLocationName(data.start)}`;


    const destinationText = document.createElement("p");

    destinationText.textContent =
        `To: ${getLocationName(data.destination)}`;


    summary.appendChild(summaryTitle);

    summary.appendChild(startText);

    summary.appendChild(destinationText);


    // Route heading.
    const title = document.createElement("h3");

    title.className = "route-title";

    title.textContent = "Follow These Steps";


    // Ordered route list.
    const list = document.createElement("ol");

    list.className = "route-list";


    // Use detailed route steps provided by Flask.
    const steps = data.route_steps || [];


    steps.forEach(step => {

        const item = document.createElement("li");


        const name = document.createElement("span");

        name.className = "route-location-name";

        name.textContent = step.name || step.id;


        item.appendChild(name);


        // Display floor and category information.
        const details = [];

        if (step.floor) {

            details.push(step.floor);

        }

        if (step.category) {

            details.push(step.category);

        }


        if (details.length > 0) {

            const detailText = document.createElement("span");

            detailText.className = "route-location-details";

            detailText.textContent = details.join(" • ");

            item.appendChild(detailText);

        }


        // Display any additional navigation notes.
        if (step.note) {

            const note = document.createElement("span");

            note.className = "route-note";

            note.textContent = step.note;

            item.appendChild(note);

        }


        list.appendChild(item);

    });


    // Display the total number of transitions.
    const total = document.createElement("div");

    total.className = "route-total";

    total.textContent =
        `Total graph transitions: ${data.total_transitions}`;


    // Explain what the route means.
    const disclaimer = document.createElement("p");

    disclaimer.className = "route-disclaimer";

    disclaimer.textContent =
        "This route follows logical campus graph connections, not GPS or measured walking distances.";


    // Add everything to the page.
    routeResult.appendChild(summary);

    routeResult.appendChild(title);

    routeResult.appendChild(list);

    routeResult.appendChild(total);

    routeResult.appendChild(disclaimer);


    // Bring the result into view.
    routeResult.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });


} catch (error) {

    console.error("Route error:", error);

    showMessage(
        error.message || "Something went wrong. Please try again.",
        "error"
    );

} finally {

    findRouteButton.disabled = false;

}
```

}

// ================================================
// 6. GET A LOCATION'S DISPLAY NAME
// ================================================

function getLocationName(locationId) {

```
const location = campusLocations.find(
    item => item.id === locationId
);

return location ? location.name : locationId;
```

}

// ================================================
// 7. SWAP START AND DESTINATION
// ================================================

function swapLocations() {

```
const currentStart = startSelect.value;

const currentDestination = destinationSelect.value;


startSelect.value = currentDestination;

destinationSelect.value = currentStart;


// Clear previous route results.
routeResult.innerHTML = "";


showMessage("Starting location and destination swapped.");
```

}

// ================================================
// 8. SEARCH CAMPUS LOCATIONS
// ================================================

async function searchLocations(event) {

```
event.preventDefault();


const query = searchInput.value.trim();


// Clear previous search results.
searchResults.innerHTML = "";


if (!query) {

    showSearchMessage("Please enter a location to search.");

    return;

}


showSearchMessage("Searching campus locations...");

searchButton.disabled = true;


try {

    const url =
        `${API_URL}/search?q=${encodeURIComponent(query)}`;


    const response = await fetch(url);

    const data = await response.json();


    if (!response.ok) {

        throw new Error("Unable to search campus locations.");

    }


    const results = data.results || [];


    if (results.length === 0) {

        showSearchMessage(
            "No matching locations found. Try another keyword."
        );

        return;

    }


    showSearchMessage(
        `${results.length} matching location(s) found.`
    );


    results.forEach(location => {

        const card = document.createElement("div");

        card.className = "search-result-item";


        const info = document.createElement("div");

        info.className = "search-result-info";


        const name = document.createElement("h3");

        name.textContent = location.name;


        const details = [];


        if (location.floor) {

            details.push(location.floor);

        }

        if (location.category) {

            details.push(location.category);

        }


        const description = document.createElement("p");

        description.textContent =
            details.length > 0
                ? details.join(" • ")
                : "Campus location";


        info.appendChild(name);

        info.appendChild(description);


        // Button to select this search result as destination.
        const useButton = document.createElement("button");

        useButton.type = "button";

        useButton.className = "use-location-button";

        useButton.textContent = "Use as Destination";


        useButton.addEventListener("click", () => {

            const exists = campusLocations.some(
                item => item.id === location.id
            );


            if (!exists) {

                showSearchMessage(
                    "This location is not available in the navigation list."
                );

                return;

            }


            destinationSelect.value = location.id;


            showSearchMessage(
                `${location.name} selected as your destination.`
            );


            // Move to the route planner.
            document.querySelector(".navigation-card").scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        });


        card.appendChild(info);

        card.appendChild(useButton);


        searchResults.appendChild(card);

    });


} catch (error) {

    console.error("Search error:", error);

    showSearchMessage(
        "Could not search locations. Check that Flask is running."
    );

} finally {

    searchButton.disabled = false;

}
```

}

// ================================================
// 9. CONNECT BUTTONS AND FORMS
// ================================================

findRouteButton.addEventListener("click", findRoute);

swapLocationsButton.addEventListener("click", swapLocations);

searchForm.addEventListener("submit", searchLocations);

// ================================================
// 10. START THE APPLICATION
// ================================================

loadLocations();
