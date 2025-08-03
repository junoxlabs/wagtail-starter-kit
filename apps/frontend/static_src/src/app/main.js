// import CSS styles
import "../css/styles.css";

// Import HTMX
import "htmx.org";

// Import Stimulus
import { Application } from "@hotwired/stimulus";

// Create a global Stimulus application
window.Stimulus = Application.start();

// You can add your custom JavaScript here
console.log("Wagtail Starter Kit - main.js loaded");
