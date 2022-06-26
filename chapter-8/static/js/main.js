import { Application } from "./vendors/stimulus.js";
import TransformerController from "./controllers/transformer_controller.js";

/*
    INITIALIZATION
*/

// Stimulus
window.Stimulus = Application.start();
Stimulus.register("transformer", TransformerController);