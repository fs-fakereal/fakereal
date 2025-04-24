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
        if (url === "/logout" || url === "/" || url === "/home") {
            window.location.href = url;
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

                // Run JavaScript from the dynamically loaded content
                runScriptsInContent(data);

                // Update browser URL without reloading the page
                if (updateHistory) {
                    history.pushState({ path: url }, "", url);
                }
            })
            .catch(error => console.error("Error loading content:", error));
    }

    // Function to execute scripts from the loaded content
    function runScriptsInContent(content) {
        const scripts = new DOMParser().parseFromString(content, 'text/html').querySelectorAll('script');
        scripts.forEach(script => {
            const newScript = document.createElement('script');
            newScript.text = script.innerText;
            document.body.appendChild(newScript); // Append the script to the document to execute it
        });
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

    // Handle internal link clicks in dynamically loaded content
document.getElementById("main-content").addEventListener("click", function (event) {
    const link = event.target.closest("a");
    if (link && link.getAttribute("href") && !link.getAttribute("href").startsWith("#") && !link.getAttribute("target")) {
        event.preventDefault();
        const url = link.getAttribute("href");
        loadPage(url);
    }
});


    // Handle browser back/forward navigation
    window.addEventListener("popstate", function (event) {
        if (event.state && event.state.path) {
            loadPage(event.state.path, false); // Load content without pushing state
        }
    });
});
