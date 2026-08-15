document.addEventListener("DOMContentLoaded", () => {
    const desktopQuery = window.matchMedia("(min-width: 992px)");

    document.querySelectorAll(".hover-dropdown").forEach((dropdown) => {
        const toggle = dropdown.querySelector(".dropdown-toggle");
        const menu = dropdown.querySelector(".dropdown-menu");

        if (!toggle || !menu) {
            return;
        }

        const setMenuState = (isOpen) => {
            if (!desktopQuery.matches) {
                menu.classList.remove("show");
                toggle.setAttribute("aria-expanded", "false");
                return;
            }

            menu.classList.toggle("show", isOpen);
            toggle.setAttribute("aria-expanded", String(isOpen));
        };

        dropdown.addEventListener("mouseenter", () => setMenuState(true));
        dropdown.addEventListener("mouseleave", () => setMenuState(false));
        dropdown.addEventListener("focusin", () => setMenuState(true));
        dropdown.addEventListener("focusout", (event) => {
            if (!dropdown.contains(event.relatedTarget)) {
                setMenuState(false);
            }
        });

        desktopQuery.addEventListener("change", () => setMenuState(false));
    });
});
