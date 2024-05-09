async function getAll() {
    // Get parameters
    let page = document.getElementById("all-page").value;
    let pageSize = document.getElementById("all-page-size").value;

    // Get data from the server
    let data = await _get("/api/creators");
    console.log(data);

     // Put the data in get-list-response
    document.getElementById("get-list-response").innerHTML = JSON.stringify(data, null, 2);
}