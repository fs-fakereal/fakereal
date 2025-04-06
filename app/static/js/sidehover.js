document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.querySelector(".sidebar");

    // Sidebar Hover Effect
    sidebar.addEventListener("mouseenter", function () {
        this.classList.add("open");
    });

    sidebar.addEventListener("mouseleave", function () {
        this.classList.remove("open");
    });

    // Function to load content dynamically without full page reload
    function loadPage(url, updateHistory = true) {
        if (url === "/logout") {
            window.location.href = url; // Full reload for logout
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

                // Update browser URL without reloading the page
                if (updateHistory) {
                    history.pushState({ path: url }, "", url);
                }
            })
            .catch(error => console.error("Error loading content:", error));
    }

    // Load default page (Upload) when page first loads
    loadPage("/upload");

    // Handle sidebar link clicks
    document.querySelectorAll(".sidebar .text-w-logo a, .sidebar .text-w-logout a").forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent full page reload
            const url = this.getAttribute("href");

            if (url && url !== "#") {
                loadPage(url);
            }
        });
    });

    // Handle browser back/forward navigation
    window.addEventListener("popstate", function (event) {
        if (event.state && event.state.path) {
            loadPage(event.state.path, false); // Load content without pushing state
        }
    });
});
