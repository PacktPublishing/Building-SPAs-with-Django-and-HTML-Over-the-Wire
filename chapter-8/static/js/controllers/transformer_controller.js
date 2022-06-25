import { Controller } from "../vendors/stimulus.js"

export default class extends Controller {

  static targets = [ "myText" ]

    connect() {
      // Connect to the WebSocket server
        this.myWebSocket = new WebSocket('ws://hello.localhost/ws/example/');
        // Listen for messages from the server
        this.myWebSocket.addEventListener("message", (event) => {
            // Parse the data received
            const data = JSON.parse(event.data);
            // Renders the HTML received from the Consumer
            const newFragment = document.createRange().createContextualFragment(data.html);
            document.querySelector(data.selector).replaceChildren(newFragment);
        });
    }

    /**
     * Transform text to uppercase
     * @param {Event} event
     * @return {void}
     */
    lowercaseToUppercase(event) {
      event.preventDefault()
      // Prepare the information we will send
      const data = {
          "action": "text in capital letters",
          "data": {
              "text": this.myTextTarget.value
          }
      };
      // Send the data to the server
      this.myWebSocket.send(JSON.stringify(data));
  }
}