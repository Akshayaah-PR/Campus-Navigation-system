// =============================================
// NCERC CAMPUS NAVIGATION SYSTEM
// Frontend JavaScript
// =============================================

const API_URL = "http://127.0.0.1:5000";


// =============================================
// 1. GET HTML ELEMENTS
// =============================================

const startSelect = document.getElementById("start");

const destinationSelect =
    document.getElementById("destination");

const findRouteButton =
    document.getElementById("findRoute");

const swapButton =
    document.getElementById("swapLocations");

const message =
    document.getElementById("message");

const routeResult =
    document.getElementById("routeResult");

const searchForm =
    document.getElementById("searchForm");

const searchInput =
    document.getElementById("searchInput");

const searchMessage =
    document.getElementById("searchMessage");

const searchResults =
    document.getElementById("searchResults");


// =============================================
// 2. LOAD CAMPUS LOCATIONS
// =============================================

async function loadLocations() {

    console.log("Connecting to the campus backend...");

    try {

        const response = await fetch(
            `${API_URL}/locations`
        );

        if (!response.ok) {
            throw new Error(
                `Backend request failed: ${response.status}`
            );
        }

        const data = await response.json();

        const locations = data.locations;

        if (!Array.isArray(locations)) {
            throw new Error(
                "The backend did not return a valid locations array."
            );
        }

        // Reset both dropdowns
        startSelect.innerHTML = "";
        destinationSelect.innerHTML = "";

        // Add default options
        startSelect.add(
            new Option("Select starting location", "")
        );

        destinationSelect.add(
            new Option("Select destination", "")
        );

        // Add campus locations
        locations.forEach(function (location) {

            const name = location.name;

            if (!name) {
                return;
            }

            startSelect.add(
                new Option(name, name)
            );

            destinationSelect.add(
                new Option(name, name)
            );

        });

        console.log(
            "Successfully loaded locations:",
            locations.length
        );

        message.textContent = "";

    } catch (error) {

        console.error(
            "Unable to load locations:",
            error
        );

        startSelect.innerHTML =
            '<option value="">Unable to load locations</option>';

        destinationSelect.innerHTML =
            '<option value="">Unable to load locations</option>';

        message.textContent =
            "Cannot connect to the backend. Check the Flask terminal.";

    }

}


// =============================================
// 3. FIND THE SHORTEST ROUTE
// =============================================

async function findRoute() {

    const start = startSelect.value;

    const destination = destinationSelect.value;

    message.textContent = "";

    routeResult.innerHTML = "";

    // Validate the input
    if (!start || !destination) {

        message.textContent =
            "Please select a starting location and destination.";

        return;

    }

    if (start === destination) {

        message.textContent =
            "Please select two different locations.";

        return;

    }

    try {

        const url =
            `${API_URL}/find-route?start=${encodeURIComponent(start)}` +
            `&destination=${encodeURIComponent(destination)}`;

        console.log("Requesting route:", url);

        const response = await fetch(url);

        const data = await response.json();

        if (!response.ok || data.error) {

            throw new Error(
                data.error || "The route could not be found."
            );

        }

        // Read the route returned by Flask
        const steps = data.route_steps || data.route;

        if (!Array.isArray(steps) || steps.length === 0) {

            throw new Error(
                "The backend did not return any route steps."
            );

        }

        // Heading
        const heading = document.createElement("h3");

        heading.textContent = "Your Shortest Route";

        routeResult.appendChild(heading);

        // =============================================
        // DISPLAY STEP-BY-STEP ROUTE
        // =============================================

        const routeList = document.createElement("ol");

        steps.forEach(function (step, index) {

            const item = document.createElement("li");

            // Handle the location returned by the backend
            if (typeof step === "string") {

             item.textContent = step;

            } else {

                // Step heading
                const heading = document.createElement("strong");

                heading.textContent =
                "STEP " + (index + 1) + ": " + step.name;

                item.appendChild(heading);

                // Navigation instruction
                if (step.instruction) {

                    const instruction = document.createElement("p");

                    instruction.textContent = step.instruction;

                    item.appendChild(instruction);

             }

                // Department information
                if (step.department) {

                    const department = document.createElement("p");

                    department.textContent =
                        "Department: " + step.department;

                    item.appendChild(department);

                }

                // Floor information
                if (step.floor) {

                    const floor = document.createElement("p");

                    floor.textContent = "Floor: " + step.floor;

                    item.appendChild(floor);

                }

            }

                routeList.appendChild(item);

        });

        routeResult.appendChild(routeList);

        // Display transition count if provided
        if (data.total_transitions !== undefined) {

            const total = document.createElement("p");

            total.textContent =
                "Total transitions: " +
                data.total_transitions;

            routeResult.appendChild(total);

        }

        console.log("Route displayed successfully.");

    } catch (error) {

        console.error(
            "Route finding error:",
            error
        );

        message.textContent =
            error.message ||
            "An error occurred while finding the route.";

    }

}


// =============================================
// 4. SEARCH CAMPUS LOCATIONS
// =============================================

async function searchLocations(event) {

    event.preventDefault();

    const query = searchInput.value.trim();

    searchResults.innerHTML = "";

    searchMessage.textContent = "";

    if (!query) {

        searchMessage.textContent =
            "Please enter a location to search.";

        return;

    }

    try {

        const url =
            `${API_URL}/search?q=${encodeURIComponent(query)}`;

        console.log("Searching:", url);

        const response = await fetch(url);

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.error || "Search request failed."
            );

        }

        const results = data.results || [];

        if (results.length === 0) {

            searchMessage.textContent =
                "No matching locations found.";

            return;

        }

        results.forEach(function (location) {

            const result = document.createElement("div");

            result.className = "search-result-item";

            const title = document.createElement("strong");

            title.textContent = location.name;

            result.appendChild(title);

            // Display building name when available
            if (location.building) {

                const building = document.createElement("p");

                building.textContent = "Building: " + location.building;

                result.appendChild(building);

            }

            // Display department
            if (location.department) {

                 const department = document.createElement("p");

                    department.textContent =
                        "Department: " + location.department;

                    result.appendChild(department);

            }

            // Display floor
            if (location.floor) {

                const floor = document.createElement("p");

                floor.textContent = "Floor: " + location.floor;

                result.appendChild(floor);

            }

            // Display category
            if (location.category) {

                const category = document.createElement("p");

                category.textContent = "Type: " + location.category;

                result.appendChild(category);

            }

            // Click a result to select the starting location
            result.addEventListener("click", function () {

                const matchingOption =
                    Array.from(startSelect.options).find(
                        option => option.textContent === location.name
                    );

                if (matchingOption) {

                    startSelect.value = matchingOption.value;

                    searchMessage.textContent =
                        location.name +
                        " selected as the starting location.";

                } else {

                    searchMessage.textContent =
                        "This result is not available in the route dropdown.";

                }

            });

            searchResults.appendChild(result);

        });

        console.log(
            "Search results:",
            results.length
        );

    } catch (error) {

        console.error(
            "Search error:",
            error
        );

        searchMessage.textContent =
            error.message ||
            "Unable to search campus locations.";

    }

}


// =============================================
// 5. SWAP LOCATIONS
// =============================================

function swapLocations() {

    const startingLocation = startSelect.value;

    const destinationLocation = destinationSelect.value;

    startSelect.value = destinationLocation;

    destinationSelect.value = startingLocation;

}


// =============================================
// 6. CONNECT BUTTONS
// =============================================

findRouteButton.addEventListener(
    "click",
    findRoute
);

swapButton.addEventListener(
    "click",
    swapLocations
);

searchForm.addEventListener(
    "submit",
    searchLocations
);


// =============================================
// 7. START THE APPLICATION
// =============================================

loadLocations();