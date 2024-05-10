async function getAll() {
    // Get parameters
    let page = document.getElementById("all-page").value;
    let pageSize = document.getElementById("all-page-size").value;

    // Get data from the server
    let data = await _get("/api/creators");
    console.log(data);

    // Display data using json-view
    const tree = jsonview.create(data);
    jsonview.render(tree, document.getElementById("get-list-response"));
    tree.id = "get-list-response-data";
}

async function getDetails() {
    // Get parameters
    let id = document.getElementById("details-id").value;

    // Get data from the server
    let data = await _get("/api/creators/" + id);
    console.log(data);

    // Display data using json-view
    const tree = jsonview.create(data);
    jsonview.render(tree, document.getElementById("get-details-response"));
    tree.id = "get-details-response-data";
}