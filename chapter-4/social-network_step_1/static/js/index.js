// Connect to WebSockets server (EchoConsumer)
const myWebSocket = new WebSocket("ws://{{ request.get_host }}/ws/social-network/");

// Event when a new message is received by WebSockets
myWebSocket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);
    // Display the message in '#welcome'
    document.querySelector("#main").innerHTML = data.html;
});