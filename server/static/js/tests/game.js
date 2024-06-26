function getListParams() {
    // Get parameters
    let page = document.getElementById("list-page").value;
    let pageSize = document.getElementById("list-page-size").value;
    let search = document.getElementById("list-search").value;
    let searchPrecise = document.getElementById("list-search-precise").checked;
    let searchExact = document.getElementById("list-search-exact").checked;
    let parentPlatforms = document.getElementById("list-parent-platforms").value;
    let platforms = document.getElementById("list-platforms").value;
    let stores = document.getElementById("list-stores").value;
    let developers = document.getElementById("list-developers").value;
    let publishers = document.getElementById("list-publishers").value;
    let genres = document.getElementById("list-genres").value;
    let tags = document.getElementById("list-tags").value;
    let creators = document.getElementById("list-creators").value;
    let dates = document.getElementById("list-dates").value;
    let updated = document.getElementById("list-updated").value;
    let platformsCount = document.getElementById("list-platforms-count").value;
    let metacritic = document.getElementById("list-metacritic").value;
    let excludeCollection = document.getElementById("list-exclude-collection").value;
    let excludeAdditions = document.getElementById("list-exclude-additions").checked;
    let excludeParents = document.getElementById("list-exclude-parents").checked;
    let excludeSeries = document.getElementById("list-exclude-game-series").checked;
    let excludeStores = document.getElementById("list-exclude-stores").value;
    let ordering = document.getElementById("list-ordering").value;
    let orderingReverse = document.getElementById("list-ordering-reverse").checked;

    // Perform validation
    if (isNaN(page) || page < 1){
        alert("Invalid page number");
        return;
    }

    if (isNaN(pageSize) || pageSize < 1){
        alert("Invalid page size");
        return;
    }

    // Perform conversion
    if (orderingReverse) {
        ordering = "-" + ordering;
    }

    // Create the parameters object
    let params = {};

    // Append if not empty
    if (page) { params.page = page; }
    if (pageSize) { params.page_size = pageSize; }
    if (search) { params.search = search; }
    if (searchPrecise) { params.search_precise = searchPrecise; }
    if (searchExact) { params.search_exact = searchExact; }
    if (parentPlatforms) { params.parent_platforms = parentPlatforms; }
    if (platforms) { params.platforms = platforms; }
    if (stores) { params.stores = stores; }
    if (developers) { params.developers = developers; }
    if (publishers) { params.publishers = publishers; }
    if (genres) { params.genres = genres; }
    if (tags) { params.tags = tags; }
    if (creators) { params.creators = creators; }
    if (dates) { params.dates = dates; }
    if (updated) { params.updated = updated; }
    if (platformsCount) { params.platforms_count = platformsCount; }
    if (metacritic) { params.metacritic = metacritic; }
    if (excludeCollection) { params.exclude_collection = excludeCollection; }
    if (excludeAdditions) { params.exclude_collection = excludeAdditions; }
    if (excludeParents) { params.exclude_parents = excludeParents; }
    if (excludeSeries) { params.exclude_game_series = excludeSeries; }
    if (excludeStores) { params.exclude_stores = excludeStores; }
    if (ordering) { params.ordering = ordering; }

    return params;
}

async function getList(){
    // Get parameters
    let params = getListParams();

    console.log(params);

    // Get the list
    let data = await _get("/api/games", params);

    // Display data using json-view
    const tree = jsonview.create(data);
    setResponse(tree, "get-list-response");
}

async function getListClass(){
    // Get parameters
    let params = getListParams();

    // Send the user to the /tests/game/list page
    window.location.href = "/tests/game/list?" + new URLSearchParams(params).toString();
}