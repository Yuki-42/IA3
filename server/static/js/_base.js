function getCookie(name) {
    // Get the value of a cookie by name
    let cookie = document.cookie.split(";").find(cookie => cookie.includes(name));
    return cookie ? cookie.split("=")[1] : "";
}

function setCookie(name, value) {
    // Set the cookie with the name to the value. Path is the root of the website
    document.cookie = `${name}=${value}; path=/;`
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

function ageCheck() {
    // Show the age modal if the user does not have an age cookie
    if (getCookie("age")) {
        return;
    }

    showAgeModal();

    // Add the event listener to the date input
    let dateInput = document.getElementById("age-input");

    dateInput.addEventListener("change", () => {
        // Get the value
        let value = dateInput.value;

        // Set the cookie
        setCookie("age", value);
    });

    // Add the event listener to the submit button
    let submitButton = document.getElementById("age-submit");

    submitButton.addEventListener("click", () => {
        // Get the value
        let value = dateInput.value;

        // Get the current date
        let now = new Date();

        // Calculate the age
        let age = now.getFullYear() - new Date(value).getFullYear();

        // Set age cookie
        setCookie("age", age);

        // Hide the modal
        hideAgeModal();
    });

    // Add the enter key event listener
    dateInput.addEventListener("keyup", event => {
        if (event.key === "Enter") {
            // Get the value
            let value = dateInput.value;

            // Get the current date
            let now = new Date();

            // Calculate the age
            let age = now.getFullYear() - new Date(value).getFullYear();

            // Set age cookie
            setCookie("age", age);

            // Hide the modal
            hideAgeModal();
        }
    });
}

function showAgeModal(){
    // Show the age modal
    let modal = document.getElementById("age-modal");
    modal.style.display = "block";
}

function hideAgeModal(){
    // Hide the age modal
    let modal = document.getElementById("age-modal");
    modal.style.display = "none";
}


// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", () => {
    // Use regex to check that the age cookie is a valid number between 0 and 150
    let age = getCookie("age");

    if (age && !/^\d+$/.test(age) || age < 0 || age > 150) {
        // If the age cookie is not a valid number between 0 and 150, delete the cookie
        document.cookie = "age=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC";
    }

    // Check the user's age
    ageCheck();
});

