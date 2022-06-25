import { Controller } from "../vendors/stimulus.js"
import { sendData } from "../webSocketsCli.js"

export default class extends Controller {

  static targets = [ "myText" ]

  /**
   * Transform text to uppercase
   * @param {Event} event
   * @return {void}
   */
  lowercaseToUppercase(event) {
      event.preventDefault()
      // Prepare the information we will send
      const newData = {
          "action": "text in capital letters",
          "data": {
              "text": this.myTextTarget.value
          }
      };
      // Send the data to the server
      sendData(newData, window.myWebSocket);
      // Clear message form
      this.myTextTarget.value = "";
  }
}