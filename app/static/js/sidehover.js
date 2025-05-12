document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.querySelector(".sidebar");
    const dashboardRoutes = ['/welcome', '/upload', '/settings', '/privacy', '/edit', '/result', '/theme']; // Removed '/dashboard'
    const standaloneRoutes = ['/logged-in/home-page'];
    
    // Store the last scan result
    let lastScanResult = localStorage.getItem('lastScanResult');
    
    // Check if current page is standalone
    const isStandalone = standaloneRoutes.some(route => window.location.pathname.startsWith(route));
    if (isStandalone) {
        return; // Exit and let the page load normally
    }

    // Only proceed with dashboard SPA functionality if not standalone
    if (sidebar) {
        // Sidebar Hover Effect
        sidebar.addEventListener("mouseenter", function() {
            this.classList.add("open");
        });

        sidebar.addEventListener("mouseleave", function() {
            this.classList.remove("open");
        });
    }

    // Function to render scan results
    function renderScanResult(content) {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = content;
        const mainContent = tempDiv.querySelector('#main-content') || tempDiv;
        document.getElementById("main-content").innerHTML = mainContent.innerHTML;
        
        mainContent.querySelectorAll('script').forEach(script => {
            const newScript = document.createElement('script');
            newScript.text = script.textContent;
            document.body.appendChild(newScript).remove();
        });
    }

    // Improved content loader
    async function loadPage(url, updateHistory = true) {
        // Force full page load for standalone routes
        if (standaloneRoutes.some(route => url.startsWith(route))) {
            window.location.href = url;
            return;
        }
        
        if (url === "/logout" || !dashboardRoutes.some(route => url.startsWith(route))) {
            window.location.href = url;
            return;
        }
        
        try {
            // Special handling for result page
            if (url === "/result") {
                if (!lastScanResult) {
                    document.getElementById("main-content").innerHTML = `
                        <div class="no-results">
                            <h2>No Scan Results Available</h2>
                            <p>Please perform a scan first to view results.</p>
                            <a href="/upload" class="btn">Go to Upload</a>
                        </div>
                    `;
                } else {
                    renderScanResult(lastScanResult);
                }
                
                if (updateHistory) {
                    history.pushState({ path: url }, '', url);
                }
                return;
            }

            const response = await fetch(url, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });

            if (!response.ok) throw new Error('Failed to load');
            
            const content = await response.text();
            
            // If this is a result page from scanning, store the result
            if (url.startsWith("/result") && content.includes('result-container')) {
                lastScanResult = content;
                localStorage.setItem('lastScanResult', content);
            }
            
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = content;
            const mainContent = tempDiv.querySelector('#main-content') || tempDiv;
            document.getElementById("main-content").innerHTML = mainContent.innerHTML;
            
            mainContent.querySelectorAll('script').forEach(script => {
                const newScript = document.createElement('script');
                newScript.text = script.textContent;
                document.body.appendChild(newScript).remove();
            });

            if (updateHistory) {
                history.pushState({ path: url }, '', url);
            }
        } catch (error) {
            console.error('Loading failed:', error);
            window.location.href = url;
        }
    }

    // Initial load - modified to handle welcome as default
    const initialPath = window.location.pathname;
    if (standaloneRoutes.some(route => initialPath.startsWith(route))) {
        // Do nothing - let it load normally
    } else if (dashboardRoutes.some(route => initialPath.startsWith(route))) {
        // Directly load whatever dashboard route we're on (including welcome)
        loadPage(initialPath, false);
    } else if (initialPath === '/dashboard') {
        // If somehow we hit dashboard, redirect to welcome
        window.location.replace('/welcome');
    } else {
        // Default to welcome page instead of dashboard
        window.location.href = "/welcome";
    }

    // Handle sidebar navigation
    if (sidebar) {
        document.querySelectorAll(".sidebar a").forEach(link => {
            link.addEventListener("click", function(e) {
                const url = this.getAttribute("href");
                if (url && url !== "#") {
                    if (standaloneRoutes.some(route => url.startsWith(route)) || url === "/logged-in" || url === "/") {
                        window.location.href = url;
                        return;
                    }
                    e.preventDefault();
                    loadPage(url);
                }
            });
        });
    }

    // Enhanced form submission handler
    document.addEventListener("submit", function(e) {
        const form = e.target;
        
        if (form.id === "UploadImage") {
            e.preventDefault();
            const formData = new FormData(form);
            const submitButton = form.querySelector('[type="submit"]');
            const originalButtonText = submitButton.value;
            
            submitButton.disabled = true;
            submitButton.value = "Processing...";
            
            fetch(form.action, {
                method: form.method,
                body: formData,
                headers: { 
                    'X-Requested-With': 'XMLHttpRequest',
                    'Cache-Control': 'no-cache'
                }
            })
            .then(response => {
                if (!response.ok) throw new Error('Upload is Successful! By clicking okay you can say as many desired images.');
                return response.text();
            })
            .then(content => {
                lastScanResult = content;
                localStorage.setItem('lastScanResult', content);
                window.location.href = "/result";
            })
            .catch(error => {
                console.error('Upload failed:', error);
                alert("Upload is Successful! By clicking okay you can say as many desired images.");
            })
            .finally(() => {
                submitButton.disabled = false;
                submitButton.value = originalButtonText;
            });
        }
        else if (form.id === "accountEditForm") {
            e.preventDefault();
            const formData = new FormData(form);
            const submitButton = form.querySelector('[type="submit"]');
            const originalButtonText = submitButton.value;
            
            submitButton.disabled = true;
            submitButton.value = "Processing...";
            
            fetch(form.action, {
                method: form.method,
                body: formData,
                headers: { 
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'text/html'
                }
            })
            .then(response => {
                if (!response.ok) throw new Error('Form submission failed');
                return response.text();
            })
            .then(content => {
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = content;
                document.getElementById("main-content").innerHTML = tempDiv.innerHTML;
                history.pushState({ path: form.action }, '', form.action);
            })
            .catch(error => {
                console.error('Form submission failed:', error);
                alert("There was an error updating your account. Please try again.");
            })
            .finally(() => {
                submitButton.disabled = false;
                submitButton.value = originalButtonText;
            });
        }
    });

    // Handle browser navigation
    window.addEventListener("popstate", function(e) {
        if (e.state && e.state.path) {
            loadPage("/welcome", false);
        } else {
            // Redirect to welcome instead of dashboard
            loadPage("/welcome", false);
        }
    });
});