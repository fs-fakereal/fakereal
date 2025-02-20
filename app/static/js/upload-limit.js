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

        const reader = new FileReader();
        reader.onload = function (e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.alt = 'Image Preview';
            previewBox.innerHTML = '';  
            previewBox.appendChild(img);
        };
        reader.readAsDataURL(file);
    } else {
        previewBox.innerHTML = '<p>No image selected</p>';
    }
}

// Handle image upload
document.getElementById("uploadForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append("image", document.getElementById("image").files[0]);

    try {
        const response = await fetch("http://localhost:3000/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        document.getElementById("message").innerText = result.message || "Upload failed";
    } catch (error) {
        console.error("Upload Error:", error);
        document.getElementById("message").innerText = "Error uploading file";
    }
});
