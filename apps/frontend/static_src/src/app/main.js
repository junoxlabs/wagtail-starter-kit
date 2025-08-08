// import CSS styles
import "../css/styles.css";

// Import HTMX
import "htmx.org";

// Import GSAP
import { gsap } from "gsap";

// Import Stimulus
import { Application } from "@hotwired/stimulus";
// Initialize Stimulus
window.Stimulus = Application.start();

// You can add your custom JavaScript here
console.log("Wagtail Starter Kit - main.js loaded");
