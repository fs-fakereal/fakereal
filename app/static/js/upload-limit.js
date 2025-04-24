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
