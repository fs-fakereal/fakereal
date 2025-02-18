document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const form = document.querySelector('form');
    const showPasswordCheckbox = document.getElementById('showPassword');

    form.addEventListener('submit', function (event) {
        // Prevent form submission if validation fails
        if (!validatePassword()) {
            event.preventDefault();
        }
    });

    function validatePassword() {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        // Check if passwords match
        if (password !== confirmPassword) {
            alert('Passwords do not match. Please try again.');
            return false;
        }

        // Define password requirements
        const minLength = 8;
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumber = /[0-9]/.test(password);
        const hasSpecialChar = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password);

        // Validate password requirements
        if (password.length < minLength) {
            alert(`Password must be at least ${minLength} characters long.`);
            return false;
        }
        if (!hasUpperCase) {
            alert('Password must contain at least one uppercase letter.');
            return false;
        }
        if (!hasLowerCase) {
            alert('Password must contain at least one lowercase letter.');
            return false;
        }
        if (!hasNumber) {
            alert('Password must contain at least one number.');
            return false;
        }
        if (!hasSpecialChar) {
            alert('Password must contain at least one special character.');
            return false;
        }

        // If all validations pass
        return true;
    }

    // Show/Hide Password Feature
    showPasswordCheckbox.addEventListener('change', function () {
        const type = this.checked ? 'text' : 'password';
        passwordInput.type = type;
        confirmPasswordInput.type = type;
    });
});
