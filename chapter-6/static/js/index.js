/*
    VARIABLES
*/
// Connect to WebSockets server (SocialNetworkConsumer)
const myWebSocket = new WebSocket(`${document.body.dataset.scheme === 'http' ? 'ws' : 'wss'}://${ document.body.dataset.host }/ws/example/`);

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
        action: 'Change page',
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
    document.querySelectorAll('.nav__link').forEach(link => {
        link.removeEventListener('click', handleClickNavigation, false);
        link.addEventListener('click', handleClickNavigation, false);
    });
}

/**
 * Send form from signup page
 * @param {Event} event
 * @return {void}
 */
function signup(event) {
    event.preventDefault();
    sendData({
        action: 'Signup',
        data: {
            username: document.querySelector('#signup-username').value,
            email: document.querySelector('#signup-email').value,
            password: document.querySelector('#signup-password').value,
            password_confirm: document.querySelector('#signup-password-confirm').value
        }
    }, myWebSocket);
}

// Event when a new message is received by WebSockets
myWebSocket.addEventListener("message", (event) => {
    // Parse the data received
    const data = JSON.parse(event.data);
    // Renders the HTML received from the Consumer
    document.querySelector(data.selector).innerHTML = data.html;
    // Update URL
    history.pushState({}, '', data.url)
    /**
     *  Reassigns the events of the newly rendered HTML
     */
    updateEvents();

});

function updateEvents() {
    setEventsNavigation(myWebSocket);
    // Singup form
    const signupForm = document.querySelector('#signup-form');
    if (signupForm !== null) {
        signupForm.removeEventListener('submit', signup, false);
        signupForm.addEventListener('submit', signup, false);
    }
}

/*
    INITIALIZATION
*/
updateEvents();
