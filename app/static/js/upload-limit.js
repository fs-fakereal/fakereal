function previewImage() {
    const fileInput = document.getElementById('image');
    const previewBox = document.getElementById('preview-box');
    const file = fileInput.files[0];

    if (file) {
        const validTypes = ['image/jpeg', 'image/png'];
        if (!validTypes.includes(file.type)) {
            alert('Please upload a valid image file (JPEG or PNG)');
            previewBox.innerHTML = '<p>No image selected</p>';
            return;
        }
    }

};

document.addEventListener("submit", function (event) {
    const form = event.target;
    if (form.id === "upload-form") {
        event.preventDefault();

        const formData = new FormData(form);

        fetch(form.action, {
            method: form.method,
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            document.getElementById("main-content").innerHTML = data;
            runScriptsInContent(data); // run any <script> tags in returned HTML
            history.pushState({ path: form.action }, "", form.action);
        })
        .catch(error => console.error("Upload failed:", error));
    }
});
