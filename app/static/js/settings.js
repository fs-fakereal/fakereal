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

function loadContent(url) {
    fetch(url)
        .then(response => response.text())
        .then(data => {
            const contentPlaceholder = document.getElementById('content-placeholder');
            contentPlaceholder.innerHTML = data;

            // Execute any <script> tags manually
            const scripts = contentPlaceholder.querySelectorAll('script');
            scripts.forEach(script => {
                const newScript = document.createElement('script');
                if (script.src) {
                    // External script
                    newScript.src = script.src;
                } else {
                    // Inline script
                    newScript.textContent = script.textContent;
                }
                document.body.appendChild(newScript); // Or append to contentPlaceholder
            });
        })
        .catch(error => {
            console.error("Error fetching the content:", error);
        });
}

