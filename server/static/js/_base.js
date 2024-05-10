function _get(url, parameters = {}) {
    // Fetch data from the server using the GET method with url arguments
    return fetch(url + "?" + new URLSearchParams(parameters), {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    }).then(response => response.json());
}

function expandAll(divId) {
    // Expand all nodes in the json-view
    let tree = document.getElementById(divId);
    tree.expand();
}