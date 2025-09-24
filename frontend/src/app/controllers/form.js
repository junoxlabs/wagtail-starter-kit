import { Controller } from "@hotwired/stimulus";

// Connects to data-controller="form"
export default class extends Controller {
  // Optional: Handle turbo events for better UX
  onTurboSubmitStart(event) {
    // Show loading indicator, disable submit button, etc.
    const submitButton = this.element.querySelector('button[type="submit"]');
    if (submitButton) {
      submitButton.disabled = true;
      submitButton.textContent = "Submitting...";
    }
  }

  onTurboSubmitEnd(event) {
    // Re-enable submit button
    const submitButton = this.element.querySelector('button[type="submit"]');
    if (submitButton) {
      submitButton.disabled = false;
      submitButton.textContent = "Submit";
    }
  }
}
