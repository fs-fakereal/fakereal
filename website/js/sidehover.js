// script.js
document.querySelector('.sidebar').addEventListener('mouseenter', function() {
    // Add 'open' class when sidebar is hovered
    this.classList.add('open');
});

document.querySelector('.sidebar').addEventListener('mouseleave', function() {
    // Remove 'open' class when sidebar is not hovered
    this.classList.remove('open');
});
