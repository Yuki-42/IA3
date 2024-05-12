function setResponse(tree, divId) {
    // Clear any existing children
    let div = document.getElementById(divId);
    div.innerHTML = "";

    // Add the new tree
    jsonview.render(tree, div);
    tree.id = divId + "-data";
}