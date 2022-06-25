import { connect, startEvents } from './webSocketsCli.js';
import { Application } from "./vendors/stimulus.js";
import transformer_controller from "./controllers/transformer_controller.js";

/*
    INITIALIZATION
*/

// WebSocket connection
connect();
startEvents();

// Stimulus
window.Stimulus = Application.start();
Stimulus.register("transformer", transformer_controller);