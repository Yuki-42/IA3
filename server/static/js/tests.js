async function getList(testType) {
    // Get parameters
    let page = document.getElementById("list-page").value;
    let pageSize = document.getElementById("list-page-size").value;

    // Get data from the server
    let data = await _get(`/api/${testType}s`);
    console.log(data);

    // Display data using json-view
    const tree = jsonview.create(data);
    setResponse(tree, "get-list-response")
}

async function getDetails(testType) {
    // Get parameters
    let id = document.getElementById("details-id").value;

    // If this is missing then display an error
    if (!id) {
        fillError(document.getElementById("get-details-response"), "Please enter an ID");
        return;
    }

    // Get data from the server
    let data = await _get(`/api/${testType}s` + id);
    console.log(data);

    // Display data using json-view
    const tree = jsonview.create(data);
    setResponse(tree, "get-details-response")
}

async function getListClass(testType) {
    // Get parameters
    let page = document.getElementById("all-page").value;
    let pageSize = document.getElementById("all-page-size").value;

    // Send the user to the /tests/creator/list page
    window.location.href = `/tests/${testType}/list?page=` + page + "&pageSize=" + pageSize;
}

async function getDetailsClass(testType) {
    // Get parameters
    let id = document.getElementById("details-id-class").value;

    // Send the user to the /tests/creator/details page
    window.location.href = `/tests/${testType}/details?id=` + id;
}