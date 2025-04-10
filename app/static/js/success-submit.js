// Wait for the document to fully load
document.addEventListener('DOMContentLoaded', function() {
    // Get the success message element
    const successMessage = document.getElementById('success-message');
    
    // If the element exists (in case the message is not set), set a timeout to hide it after 5 seconds
    if (successMessage) {
        setTimeout(function() {
            successMessage.style.display = 'hidden';
        }, 2000); // 5000 milliseconds = 5 seconds
    }
});