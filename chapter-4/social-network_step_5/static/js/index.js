/*
    VARIABLES
*/
// Connect to WebSockets server (SocialNetworkConsumer)
const myWebSocket = new WebSocket(`${document.body.dataset.scheme === 'http' ? 'ws' : 'wss'}://${ document.body.dataset.host }/ws/social-network/`);
const inputAuthor = document.querySelector("#message-form__author");
const inputText = document.querySelector("#message-form__text");
const inputSubmit = document.querySelector("#message-form__submit");
const nextPageButton = document.querySelector("#messages__next-page");
const previousPageButton = document.querySelector("#messages__previous-page");
let currentPage = 1;

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

/**
 * Delete message
 * @param {Event} event
 * @return {void}
 */
function deleteMessage(event) {
    const message = {
        "action": "delete message",
        "data": {
            "id": event.target.dataset.id
        }
    };
    sendData(message, myWebSocket);
}

/**
 * Send new message
 * @param {Event} event
 * @return {void}
 */
function sendNewMessage(event) {
    event.preventDefault();
    // Prepare the information we will send
    const newData = {
        "action": "add message",
        "data": {
            "author": inputAuthor.value,
            "text": inputText.value
        }
    };
    // Send the data to the server
    sendData(newData, myWebSocket);
    // Clear message form
    inputText.value = "";
}

/**
 * Switch to the next page
 * @param {Event} event
 * @return {void}
 */
function goToNextPage(event) {
    // Increment current page
    currentPage += 1;
    // Activate the back button if we are not on the first page
    if (currentPage !== 1) {
        previousPageButton.removeAttribute("disabled");
    }
    // Prepare the information we will send
    const newData = {
        "action": "list messages",
        "data": {
            "page": currentPage,
        }
    };
    // Send the data to the server
    sendData(newData, myWebSocket);
}

/**
 * Switch to the previous page
 * @param {Event} event
 * @return {void}
 */
function goToPreviousPage(event) {
    if (currentPage > 1) {
        // Page back
        currentPage -= 1;
        // Deactivate the button if we are on the first page
        if (currentPage === 1) {
            previousPageButton.setAttribute("disabled", true);
        }
        // Prepare the information we will send
        const newData = {
            "action": "list messages",
            "data": {
                "page": currentPage,
            }
        };
        // Send the data to the server
        sendData(newData, myWebSocket);
    }
}

/*
    EVENTS
*/

// Event when a new message is received by WebSockets
myWebSocket.addEventListener("message", (event) => {
    // Parse the data received
    const data = JSON.parse(event.data);
    // Renders the HTML received from the Consumer
    document.querySelector(data.selector).innerHTML = data.html;
    // Add to all delete buttons the event
    document.querySelectorAll(".messages__delete").forEach(button => {
        button.addEventListener("click", deleteMessage);
    });
});

// Sends new message when you click on Submit
inputSubmit.addEventListener("click", sendNewMessage);

// Pagination
nextPageButton.addEventListener("click", goToNextPage);
previousPageButton.addEventListener("click", goToPreviousPage);

/*
    INITIALIZATION
*/