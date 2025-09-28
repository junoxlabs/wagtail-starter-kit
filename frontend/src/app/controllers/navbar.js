import { Controller } from "@hotwired/stimulus";
import { gsap } from "gsap";

//! connects to data-controller="navbar"
export default class extends Controller {
  static animationDuration = 0.2; // seconds
  static easeIn = "power3.in";
  static easeOut = "power3.out";

  // targets for the mobile menu and icons within the navbar
  static targets = ["mobileMenu", "hamburgerIcon", "closeIcon"];

  connect() {
    gsap.set(this.mobileMenuTarget, { autoAlpha: 0 });
  }

  toggleMenu() {
    const isHidden = this.mobileMenuTarget.classList.contains("hidden");

    if (isHidden) {
      this.mobileMenuTarget.classList.remove("hidden");
      this.hamburgerIconTarget.classList.add("hidden");
      this.closeIconTarget.classList.remove("hidden");

      gsap.to(this.mobileMenuTarget, {
        autoAlpha: 1,
        duration: this.constructor.animationDuration,
        ease: this.constructor.easeOut,
      });
    } else {
      this.closeMenu();
    }
  }

  // if a user clicks a link in the mobile menu, it closes it.
  //! data-action="click->navbar#closeMenu" to your <a> tags in the mobile menu
  closeMenu() {
    this.hamburgerIconTarget.classList.remove("hidden");
    this.closeIconTarget.classList.add("hidden");

    gsap.to(this.mobileMenuTarget, {
      autoAlpha: 0,
      duration: this.constructor.animationDuration,
      ease: this.constructor.easeIn,

      onComplete: () => {
        this.mobileMenuTarget.classList.add("hidden");
      },
    });
  }

  //! handles mobile menu dropdown animations
  toggleMobileDropdown(event) {
    // Prevent the default behavior to control the open state manually
    event.preventDefault();

    // Get the clicked summary element (the dropdown header/button)
    // This is the element that was clicked to trigger the dropdown toggle
    const summary = event.currentTarget;

    // Find the parent <details> element containing this summary
    // This allows us to work with the specific dropdown that was clicked
    const details = summary.closest("details");

    // Find the content element (ul) inside the details element
    // This is the dropdown content that will be animated
    const content = details.querySelector("ul");

    if (details.open) {
      // Dropdown is currently open, so we're closing it
      gsap.to(content, {
        // Animate the max-height to 0 to create the closing effect
        maxHeight: 0,
        duration: this.constructor.animationDuration,
        ease: this.constructor.easeOut,

        // Callback function that runs when the animation completes
        onComplete: () => {
          // Set overflow to hidden after animation completes to properly hide content
          // This prevents any content from being visible when the dropdown is closed
          content.style.overflow = "hidden";
          // Now that animation is complete, close the details element
          details.removeAttribute("open");
        },
      });

      // Rotate icon - find the SVG icon in the summary element
      const icon = summary.querySelector("svg");
      if (icon) {
        // Animate the icon rotation from 180 degrees back to 0 degrees
        // This provides visual feedback that the dropdown is closing
        gsap.to(icon, {
          rotation: 0, // Reset rotation to 0 degrees (arrow pointing right/down)
          duration: this.constructor.animationDuration,
          ease: this.constructor.easeOut,
        });
      }
    } else {
      // Dropdown is currently closed, so we're opening it
      // Set overflow to hidden to prevent content from being visible during animation setup
      content.style.overflow = "hidden";
      // Set initial max-height to 0 before starting the animation
      // This ensures the dropdown starts from a closed state
      gsap.set(content, { maxHeight: 0 });

      // Open the details element first so content is visible for animation
      details.setAttribute("open", "");

      gsap.to(content, {
        // Calculate the scroll height and add 100px buffer for safety
        // This ensures all content is visible when the dropdown opens
        maxHeight: content.scrollHeight + 100, // Add buffer
        duration: this.constructor.animationDuration,
        ease: this.constructor.easeOut,
      });

      // Rotate icon - find the SVG icon in the summary element
      const icon = summary.querySelector("svg");
      if (icon) {
        // Animate the icon rotation from 0 degrees to 180 degrees
        // This provides visual feedback that the dropdown is opening
        gsap.to(icon, {
          rotation: 180, // Rotate to 180 degrees (arrow pointing up)
          duration: this.constructor.animationDuration,
          ease: this.constructor.easeOut,
        });
      }
    }
  }
}
