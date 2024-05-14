async function getList(endpoint) {
    // Get parameters
    let page = document.getElementById("list-page").value;
    let pageSize = document.getElementById("list-page-size").value;

    // Get data from the server
    let data = await _get(`/api/${endpoint}s`);
    console.log(data);

    // Display data using json-view
    const tree = jsonview.create(data);
    setResponse(tree, "get-list-response")
}

async function getDetails(endpoint) {
    // Get parameters
    let id = document.getElementById("details-id").value;

    // If this is missing then display an error
    if (!id) {
        fillError(document.getElementById("get-details-response"), "Please enter an ID");
        return;
    }

    // Get data from the server
    let data = await _get(`/api/${endpoint}s/` + id);
    console.log(data);

    // Display data using json-view
    const tree = jsonview.create(data);
    setResponse(tree, "get-details-response")
}

async function getListClass(endpoint) {
    // Get parameters
    let page = document.getElementById("list-page-class").value;
    let pageSize = document.getElementById("list-page-size-class").value;

    // Send the user to the /tests/developer/list page
    window.location.href = `/tests/${endpoint}/list?page=` + page + "&pageSize=" + pageSize;
}

async function getDetailsClass(endpoint) {
    // Get parameters
    let id = document.getElementById("details-id-class").value;

    // Send the user to the /tests/developer/details page
    window.location.href = `/tests/${endpoint}/details?id=` + id;
}