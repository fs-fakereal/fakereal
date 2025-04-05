document.addEventListener("DOMContentLoaded", function () {
    // Select all links
    const links = document.querySelectorAll('.tile-link');

    // Iterate through each link and prevent default reload behavior
    links.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();  // Prevent the default page reload

            // Get the URL for the link's href attribute
            const url = link.getAttribute('href');

            // Call the function to dynamically load the content
            loadContent(url);
        });
    });
});

// Function to dynamically load the content
function loadContent(url) {
    // Fetch the content for the clicked link's URL
    fetch(url)
        .then(response => response.text())  // Get the HTML content as text
        .then(data => {
            // Get the placeholder div where content will be injected
            const contentPlaceholder = document.getElementById('content-placeholder');
            // Insert the fetched content into the placeholder
            contentPlaceholder.innerHTML = data;
        })
        .catch(error => {
            console.error("Error fetching the content:", error);
        });
}
