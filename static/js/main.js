document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("registerForm");

    if (registerForm) {
        registerForm.addEventListener("submit", (event) => {
            const password = registerForm.querySelector('[name="password"]').value;

            if (password.length < 6) {
                event.preventDefault();
                alert("Password must contain at least 6 characters.");
            }
        });
    }
});
