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
    // Navigation
    document.querySelectorAll('.nav__link--page').forEach(link => {
        link.removeEventListener('click', handleClickNavigation, false);
        link.addEventListener('click', handleClickNavigation, false);
    });
    // Logout
    const buttonLogout = document.querySelector('#logout');
    if (buttonLogout !== null) {
        buttonLogout.addEventListener('click', logout, false);
    }
}


/**
 * Send message to Logout
 * @param {Event} event
 * @return {void}
 */
function logout(event) {
    event.preventDefault();
    sendData({
        action: 'Logout',
        data: {}
    }, myWebSocket);
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


/**
 * Send form from login page
 * @param {Event} event
 * @return {void}
 */
function login(event) {
    event.preventDefault();
    sendData({
        action: 'Login',
        data: {
            email: document.querySelector('#login-email').value,
            password: document.querySelector('#login-password').value
        }
    }, myWebSocket);
}


/**
 * Send new Lap
 * @param {Event} event
 * @return {void}
 */
function addLap(event) {
    sendData({
        action: 'Add lap',
        data: {}
    }, myWebSocket);
}

/**
 * Send new task to TODO list
 * @param event
 * @return {void}
 */
function addTask(event) {
    const task = document.querySelector('#task');
    sendData({
        action: 'Add task',
        data: {
            task: task.value
        }
    }, myWebSocket);
    // Clear input
    task.value = '';
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
    history.pushState({}, '', data.url)
    /**
     *  Reassigns the events of the newly rendered HTML
     */
    updateEvents();
});

/**
 * Update events in every page
 * return {void}
 */
function updateEvents() {
    // Nav
    setEventsNavigation(myWebSocket);
    // Singup form
    const signupForm = document.querySelector('#signup-form');
    if (signupForm !== null) {
        signupForm.removeEventListener('submit', signup, false);
        signupForm.addEventListener('submit', signup, false);
    }
    // Login
    const loginForm = document.querySelector('#login-form');
    if (loginForm !== null) {
        loginForm.removeEventListener('submit', login, false);
        loginForm.addEventListener('submit', login, false);
    }
    // Add lap
    const addLapButton = document.querySelector('#add-lap');
    if (addLapButton !== null) {
        addLapButton.removeEventListener('click', addLap, false);
        addLapButton.addEventListener('click', addLap, false);
    }
    // Add task
    const addTaskButton = document.querySelector('#add-task');
    if (addTaskButton !== null) {
        addTaskButton.removeEventListener('click', addTask, false);
        addTaskButton.addEventListener('click', addTask, false);
    }
}

/*
    INITIALIZATION
*/
updateEvents();
