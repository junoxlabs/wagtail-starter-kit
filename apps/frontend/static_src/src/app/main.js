// import CSS styles
import "../css/styles.css";

// Import HTMX
import "htmx.org";

// Import GSAP
import { gsap } from "gsap";

// Import Stimulus
import { Application } from "@hotwired/stimulus";

// start Stimulus application
const app = Application.start();

// Auto-register Stimulus controllers
const context = require.context("./controllers", true, /\.js$/);
context.keys().forEach((filename) => {
  // Convert the filename to a controller name
  const controllerName = filename
    // Remove the leading "./"
    .replace(/^\.\//, "")
    // Remove the ".js" extension
    .replace(/\.js$/, "")
    // Replace underscores with dashes
    .replace(/_/g, "-")
    // Replace slashes with double dashes
    .replace(/\//g, "--");

  // Import the controller module
  const module = context(filename);
  // Register the controller with the Stimulus application
  app.register(controllerName, module.default);
});

// Expose Stimulus application globally
window.Stimulus = app;
