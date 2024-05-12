async function getList() {
    // Get parameters
    let page = document.getElementById("list-page").value;
    let pageSize = document.getElementById("list-page-size").value;

    // Get data from the server
    let data = await _get("/api/creators");
    console.log(data);

    // Display data using json-view
    const tree = jsonview.create(data);
    setResponse(tree, "get-list-response")
}

async function getDetails() {
    // Get parameters
    let id = document.getElementById("details-id").value;

    // Get data from the server
    let data = await _get("/api/creators/" + id);
    console.log(data);

    // Display data using json-view
    const tree = jsonview.create(data);
    setResponse(tree, "get-details-response")
}

async function getListClass() {
    // Get parameters
    let page = document.getElementById("all-page").value;
    let pageSize = document.getElementById("all-page-size").value;

    // Send the user to the /tests/creator/list page
    window.location.href = "/tests/creator/list?page=" + page + "&pageSize=" + pageSize;
}

async function getDetailsClass() {
    // Get parameters
    let id = document.getElementById("details-id-class").value;

    // Send the user to the /tests/creator/details page
    window.location.href = "/tests/creator/details?id=" + id;
}