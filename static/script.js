/**
 * AI Vocabulary Assistant - Frontend JavaScript
 */

document.addEventListener("DOMContentLoaded", function () {
    initializePasswordToggle();
    initializeFormValidation();
    initializeAnimations();
    initializeModals();
});


/* ==========================
   SHOW PASSWORD
========================== */

function initializePasswordToggle() {
    const checkboxes = document.querySelectorAll(".show-password");

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            const targetId = this.getAttribute("data-target");
            const passwordInput = document.getElementById(targetId);

            if (!passwordInput) return;

            passwordInput.type = this.checked ? "text" : "password";
        });
    });

    const iconButtons = document.querySelectorAll("[data-toggle-password]");

    iconButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            const targetId = this.getAttribute("data-target");
            let passwordInput = null;

            if (targetId) {
                passwordInput = document.getElementById(targetId);
            } else {
                passwordInput = this.previousElementSibling;
            }

            if (!passwordInput) return;

            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                this.textContent = "🙈";
            } else {
                passwordInput.type = "password";
                this.textContent = "👁️";
            }
        });
    });
}


/* ==========================
   FORM VALIDATION
========================== */

function initializeFormValidation() {
    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {
        form.addEventListener("submit", function (e) {
            if (!validateForm(form)) {
                e.preventDefault();
                showNotification("Please fill in all required fields.", "error");
            }
        });
    });
}

function validateForm(form) {
    const inputs = form.querySelectorAll("input[required]");
    let isValid = true;

    inputs.forEach(function (input) {
        if (!input.value.trim()) {
            input.style.borderColor = "#ff6b6b";
            isValid = false;
        } else {
            input.style.borderColor = "rgba(124, 200, 94, 0.5)";
        }
    });

    return isValid;
}


/* ==========================
   ANIMATIONS
========================== */

function initializeAnimations() {
    const elements = document.querySelectorAll("[data-animate]");

    elements.forEach(function (element, index) {
        element.style.opacity = "0";
        element.style.transform = "translateY(20px)";
        element.style.transition = "all 0.5s ease";

        setTimeout(function () {
            element.style.opacity = "1";
            element.style.transform = "translateY(0)";
        }, index * 100);
    });
}


/* ==========================
   MODALS
========================== */

function initializeModals() {
    const closeButtons = document.querySelectorAll("[data-close-modal]");

    closeButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            const modal = this.closest("[data-modal]");
            if (modal) {
                modal.style.display = "none";
            }
        });
    });

    document.addEventListener("click", function (e) {
        if (e.target.hasAttribute("data-modal")) {
            e.target.style.display = "none";
        }
    });
}


/* ==========================
   HELPERS
========================== */

function showConfirmDialog(message, onConfirm) {
    if (confirm(message)) {
        onConfirm();
    }
}

function debounce(func, wait) {
    let timeout;

    return function (...args) {
        clearTimeout(timeout);

        timeout = setTimeout(function () {
            func.apply(this, args);
        }, wait);
    };
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function () {
        showNotification("Copied to clipboard!", "success");
    }).catch(function () {
        showNotification("Failed to copy", "error");
    });
}

function showNotification(message, type = "info") {
    const notification = document.createElement("div");

    notification.className = "notification notification-" + type;
    notification.textContent = message;

    let background = "#4a9eff";

    if (type === "success") {
        background = "#7cc85e";
    }

    if (type === "error") {
        background = "#ff6b6b";
    }

    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${background};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        z-index: 9999;
        font-weight: 600;
    `;

    document.body.appendChild(notification);

    setTimeout(function () {
        notification.remove();
    }, 3000);
}

function truncateText(text, maxLength = 100) {
    if (!text) return "";
    return text.length > maxLength ? text.substring(0, maxLength) + "..." : text;
}

function highlightText(text, searchTerm) {
    if (!searchTerm) return text;

    const regex = new RegExp("(" + searchTerm + ")", "gi");
    return text.replace(regex, "<mark>$1</mark>");
}


/* ==========================
   EXPORTS
========================== */

window.copyToClipboard = copyToClipboard;
window.showNotification = showNotification;
window.showConfirmDialog = showConfirmDialog;
window.truncateText = truncateText;
window.highlightText = highlightText;