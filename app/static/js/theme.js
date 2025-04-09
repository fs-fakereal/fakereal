// Set the theme based on localStorage or default to light mode
function setThemeFromStorage() {
    const savedTheme = localStorage.getItem('theme'); // Retrieve theme from localStorage
    if (savedTheme) {
        document.body.classList.add(savedTheme); // Apply the saved theme class (either dark-mode or light-mode)
    } else {
        document.body.classList.add('light-mode'); // Default to light mode if no theme is saved
    }
}

// Switch between light and dark modes
function setTheme(theme) {
    const body = document.body;

    // Remove both theme classes first
    body.classList.remove('light-mode', 'dark-mode');

    // Add the new theme class based on selection
    if (theme === 'dark') {
        body.classList.add('dark-mode');
    } else {
        body.classList.add('light-mode');
    }

    // Save the theme choice to localStorage
    localStorage.setItem('theme', theme);
}

// Listen for changes and apply theme when user selects an option
document.getElementById('light-mode-btn')?.addEventListener('click', function () {
    console.log('Light Mode selected');
    setTheme('light');
});

document.getElementById('dark-mode-btn')?.addEventListener('click', function () {
    console.log('Dark Mode selected');
    setTheme('dark');
});

// Save changes and redirect to the dashboard (or any other page)
document.getElementById('save-changes-btn')?.addEventListener('click', function () {
    console.log('Save Changes button clicked'); // Debugging log
    window.location.href = '/dashboard'; // Redirect back to the dashboard
});

// Apply the saved theme on page load for all pages
window.onload = setThemeFromStorage;
