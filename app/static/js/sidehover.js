document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.querySelector(".sidebar");

    // Sidebar Hover Effect
    sidebar.addEventListener("mouseenter", function () {
        this.classList.add("open");
    });

    sidebar.addEventListener("mouseleave", function () {
        this.classList.remove("open");
    });

    // Function to load content dynamically
    function loadPage(url) {
        if (url === "/logout") {
            window.location.href = url; // Force full page reload for logout
            return;
        }

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Page not found");
                }
                return response.text();
            })
            .then(data => {
                document.getElementById("main-content").innerHTML = data;
            })
            .catch(error => console.error("Error loading content:", error));
    }

    // Load "Upload" as the default page
    loadPage("/upload"); // Ensure "/upload" is correct in your Flask routes

    // Handle Sidebar Link Clicks
    document.querySelectorAll(".sidebar ul li a").forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent full page refresh
            const url = this.getAttribute("href");

            if (url && url !== "#") {
                loadPage(url);
            }
        });
    });
});
