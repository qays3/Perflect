// openvpn.js

document.getElementById('generateVPNButton').addEventListener('click', function () {
    const generateVPNButton = document.getElementById('generateVPNButton');
    const statusMessage = document.getElementById('statusMessage');
 
    generateVPNButton.classList.add("reloading");
    generateVPNButton.style.pointerEvents = "none";

    statusMessage.innerHTML = 'Generating your OpenVPN file...';

    fetch('/generate_openvpn', {
        method: 'POST',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to generate OpenVPN file.');
        }
        return response.blob();
    })
    .then(blob => {
     
        const downloadLink = document.createElement('a');
        downloadLink.href = URL.createObjectURL(blob);
        downloadLink.download = 'client.ovpn';
        downloadLink.click();

        statusMessage.innerHTML = 'OpenVPN file has been downloaded!';
    })
    .catch(error => {
        console.error('Error:', error);
        statusMessage.innerHTML = 'An error occurred while generating the OpenVPN file.';
    })
    .finally(() => {
        
        generateVPNButton.classList.remove("reloading");
        generateVPNButton.style.pointerEvents = "auto";
    });
});