// startups.js

let selectedFile = null;

function updateFileName(event) {
    const fileNameDisplay = document.getElementById('fileNameDisplay');
    const file = event.target.files[0];

    if (file) {
        selectedFile = file;
        fileNameDisplay.textContent = `Selected file: ${file.name}`;
    } else {
        selectedFile = null;
        fileNameDisplay.textContent = 'No file selected';
    }
}

async function uploadFile() {
    const uploadButton = document.getElementById('uploadButton');
    if (!selectedFile) {
        document.getElementById('statusMessage').textContent = 'Please select a valid file.';
        return;
    }

   
    uploadButton.classList.add("reloading");
    uploadButton.style.pointerEvents = "none";

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch('/syscontrols/add', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            document.getElementById('statusMessage').textContent = result.status;
            showMessageBox("File added to startup successfully!");
        } else {
            document.getElementById('statusMessage').textContent = result.detail || 'An error occurred.';
        }
    } catch (error) {
        document.getElementById('statusMessage').textContent = 'Failed to upload the file. Please try again.';
    } finally {
       
        uploadButton.classList.remove("reloading");
        uploadButton.style.pointerEvents = "auto";
    }
}

function showMessageBox(message) {
    const messageBox = document.getElementById('messageBox');
    messageBox.textContent = message;
    messageBox.style.display = 'block';
    setTimeout(() => {
        messageBox.style.display = 'none';
    }, 5000);
}