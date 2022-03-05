// Connect to WebSockets server (EchoConsumer)
const myWebSocket = new WebSocket(`${document.body.dataset.scheme === 'http' ? 'ws' : 'wss'}://${ document.body.dataset.host }/ws/example/`);

// Event when a new message is received by WebSockets
myWebSocket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);
    // Display the message in '#welcome'
    document.querySelector("#main").innerHTML = data.html;
});