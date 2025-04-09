
window.addEventListener('DOMContentLoaded', function() {
    const genForm = document.querySelector("form #uploadForm");
    genForm.addEventListener('submit', uploadFile);

    async function uploadFile(event) {
        event.preventDefault();


        const formData = new FormData(genForm);

        if (!file) {
            alert("No file found.");
            return;
        }

        let data = new FormData();
        data.append('file', file);

        try {
            const res = await fetch('/upload', {
                method: 'POST',
                body: formData
            })
            if (!res.ok) {
                throw new Error(`${res.status}: ${await res.text()}`)
            }

            const data = await res.json();

            console.log(data);
        }
        catch (err) {
            console.error(err);
            alert('An error occurred during upload.');
        }
    }

}
)