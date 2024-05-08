async function _get(url) {
    // Gets the json return from a GET request without using XMLHttpRequest
    let response = await fetch(url);
    return await response.json();
}