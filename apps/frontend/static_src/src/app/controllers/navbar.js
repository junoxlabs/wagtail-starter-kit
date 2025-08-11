import { Controller } from "@hotwired/stimulus";
import { gsap } from "gsap";

//! connects to data-controller="navbar"
export default class extends Controller {
  // Define the targets that this controller will interact with in your HTML
  static targets = ["mobileMenu", "hamburgerIcon", "closeIcon"];
  static animationDuration = 0.2; // seconds

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
        ease: "power2.out",
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
      ease: "power2.in",

      onComplete: () => {
        this.mobileMenuTarget.classList.add("hidden");
      },
    });
  }
}
