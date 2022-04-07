/*
    VARIABLES
*/
// Connect to WebSockets server (SocialNetworkConsumer)
const myWebSocket = new WebSocket(`${document.body.dataset.scheme === 'http' ? 'ws' : 'wss'}://${ document.body.dataset.host }/ws/chat/`);

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
 * Send message to WebSockets server
 * @return {void}
 */
function sendNewMessage(event) {
    event.preventDefault();
    const messageText = document.querySelector('#message-text')
    sendData({
            action: 'New message',
            data: {
                message: messageText.value
            }
        }, myWebSocket);
    messageText.value = '';
}

/**
 * Requests the Consumer to change the group with respect to the Dataset group-name.
 * @param event
 */
function changeGroup(event) {
    event.preventDefault();
    sendData({
            action: 'Change group',
            data: {
                groupName: event.target.dataset.groupName,
                isGroup: event.target.dataset.groupPublic === "true"
            }
        }, myWebSocket);
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
    // Scrolls to the bottom of the chat
    const messagesList = document.querySelector('#messages-list');
    messagesList.scrollTop = messagesList.scrollHeight;
    /**
     *  Reassigns the events of the newly rendered HTML
     */
    // Button to send new message button
    document.querySelector('#send').addEventListener('click', sendNewMessage);
    // Buttons for changing groups
    document.querySelectorAll(".nav__link").forEach(button => {
        button.addEventListener("click", changeGroup);
    });
});