function getCookie(name) {
    // Get the value of a cookie by name
    let cookie = document.cookie.split(";").find(cookie => cookie.includes(name));
    return cookie ? cookie.split("=")[1] : "";
}

function setCookie(name, value) {
    // Set the cookie with the name to the value. Path is the root of the website
    document.cookie = `${name}=${value}; path=/;`
}


function toggleTheme() {
    // Get the current theme
    let theme = getCookie("theme");

    // Set the theme to the opposite of the current theme
    if (theme === "dark") {
        setCookie("theme", "light");
    } else {
        setCookie("theme", "dark");
    }

    // Reload the stylesheets
    reloadColours();
}


function _get(url, parameters = {}) {
    console.log(url)
    // Fetch data from the server using the GET method with url arguments
    return fetch(url + "?" + new URLSearchParams(parameters), {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*" // Allow CORS
        }
    }).then(response => {
        // Capture the response to perform multiple operations
        let clone = response.clone();
        clone.text().then(text => {
            console.log("Server response: ", text);
        });
        return response.json();
    });
}

function reloadColours() {
    let colours = document.getElementById("colours");

    colours.href = colours.href.replace(/\?.*|$/, "?reload=" + new Date().getTime());
}


// Adds a child div with the message to the parent div
function fillError(div, message) {
    // Create a new div
    let error = document.createElement("div");

    // Set the class of the div
    error.className = "error";

    // Set the text of the div
    error.innerText = message;

    // Clear any children of the parent div with the same class
    div.querySelectorAll(".error").forEach(element => element.remove());

    // Append the new div to the parent div
    div.appendChild(error);
}

// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", () => {
    // Get the current theme
    let theme = getCookie("theme");

    // Get the theme toggle element
    let themeToggle = document.getElementById("theme-selector-checkbox");

    // Set the theme toggle to the current theme
    themeToggle.checked = theme === "dark";

    // Add the event listener to the theme toggle
    themeToggle.addEventListener("change", toggleTheme);
});

