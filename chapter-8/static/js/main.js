import { Application } from "./vendors/stimulus.js";
import transformer_controller from "./controllers/transformer_controller.js";

/*
    INITIALIZATION
*/

// Stimulus
window.Stimulus = Application.start();
Stimulus.register("transformer", transformer_controller);