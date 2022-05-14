/*
    VARIABLES
*/
// Connect to WebSockets server (SocialNetworkConsumer)
const myWebSocket = new WebSocket(`${document.body.dataset.scheme === "http" ? "ws" : "wss"}://${ document.body.dataset.host }/ws/blog/`);

/*
    FUNCTIONS
*/

/**
 * Send data to WebSockets server
 * @param {string} message
 * @param {WebSocket} webSocket
 * @return {void}
 */
function sendData(message, webSocket) {
    webSocket.send(JSON.stringify(message));
}

/*
    EVENTS
*/

/**
 * Send message to update page
 * @param {Event} event
 * @return {void}
 */
function handleClickNavigation(event) {
    event.preventDefault();
    sendData({
        action: "Change page",
        data: {
            page: event.target.dataset.target
        }
    }, myWebSocket);
}

/**
 * Send message to WebSockets server to change the page
 * @param {WebSocket} webSocket
 * @return {void}
 */
function setEventsNavigation(webSocket) {
    // Navigation
    document.querySelectorAll(".nav__link--page").forEach(link => {
        link.removeEventListener("click", handleClickNavigation, false);
        link.addEventListener("click", handleClickNavigation, false);
    });
    // Logout
    const buttonLogout = document.querySelector("#logout");
    if (buttonLogout !== null) {
        buttonLogout.addEventListener("click", logout, false);
    }
}


// Event when a new message is received by WebSockets
myWebSocket.addEventListener("message", (event) => {
    // Parse the data received
    const data = JSON.parse(event.data);
    // Renders the HTML received from the Consumer
    const selector = document.querySelector(data.selector);
    // If append is received, it will be appended. Otherwise the entire DOM will be replaced.
    if (data.append) {
        selector.innerHTML += data.html;
    } else {
        selector.innerHTML = data.html;
    }
    // Update URL
    history.pushState({}, "", data.url)
    /**
     *  Reassigns the events of the newly rendered HTML
     */
    updateEvents();
});


/**
 * Event to request a search
 * @param event
 */
function search(event) {
    event.preventDefault();
    const search = event.target.querySelector("#search").value;
    sendData({
        action: "Search",
        data: {
            search: search
        },
    }, myWebSocket);
}


/**
 * Event to add a next page with the pagination
 * @param event
 */
function addNextPaginator(event) {
    const nextPage = event.target.dataset.nextPage;
    sendData({
        action: "Add new posts",
        data: {
            page: nextPage
        },
    }, myWebSocket);
}


/**
 * Update events in every page
 * return {void}
 */
function updateEvents() {
    // Nav
    setEventsNavigation(myWebSocket);
    // Search form
    const searchForm = document.querySelector("#search-form");
    if (searchForm !== null) {
        searchForm.removeEventListener("submit", search, false);
        searchForm.addEventListener("submit", search, false);
    }
    // Paginator
    const paginator = document.querySelector("#paginator");
    if (paginator !== null) {
        paginator.removeEventListener("click", addNextPaginator, false);
        paginator.addEventListener("click", addNextPaginator, false);
    }
}

/*
    INITIALIZATION
*/
updateEvents();
