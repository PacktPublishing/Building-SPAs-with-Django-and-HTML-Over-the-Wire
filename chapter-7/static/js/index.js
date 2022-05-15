/*
    VARIABLES
*/
// Connect to WebSockets server (SocialNetworkConsumer)
const myWebSocket = new WebSocket(`${document.body.dataset.scheme === "http" ? "ws" : "wss"}://${ document.body.dataset.host }/ws/blog/`);

/*
    FUNCTIONS
*/


/**
 * @description
 * @param {Event} event
 * @returns {void}
 */
function changePage(event) {
    event.preventDefault();
    sendData({
        action: "Change page",
        data: {
            page: event.target.dataset.page,
            id: event.target.dataset.id
        }
    }, myWebSocket);
}


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
}


// Event when a new message is received by WebSockets
myWebSocket.addEventListener("message", (event) => {
    // Parse the data received
    const data = JSON.parse(event.data);
    // Renders the HTML received from the Consumer
    const selector = document.querySelector(data.selector);
    // We only allow all users to render if we receive a broadcast as true and it is at the same url.
    if (
        data.broadcast === undefined ||
        !data.broadcast ||
        (data.broadcast && data.url === document.location.pathname)
        ) {
        // If append is received, it will be appended. Otherwise the entire DOM will be replaced.
        if (data.append) {
            selector.innerHTML += data.html;
        } else {
            selector.innerHTML = data.html;
        }
        // Update URL
        history.pushState({}, "", data.url)
    }

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
        action: "Add next posts",
        data: {
            page: nextPage
        },
    }, myWebSocket);
}


function addComment(event) {
    event.preventDefault();
    const author = event.target.querySelector("#author").value;
    const content = event.target.querySelector("#content").value;
    const postId = event.target.dataset.postId;
    sendData({
        action: "Add comment",
        data: {
            author: author,
            content: content,
            post_id: postId
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
    // Comment form
    const commentForm = document.querySelector("#comment-form");
    if (commentForm !== null) {
        commentForm.removeEventListener("submit", addComment, false);
        commentForm.addEventListener("submit", addComment, false);
    }
    // Link to single post
    const linksPostItem = document.querySelectorAll(".post-item__link");
    if (linksPostItem !== null) {
        linksPostItem.forEach(link => {
            link.removeEventListener("click", changePage, false);
            link.addEventListener("click", changePage, false);
        });
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
