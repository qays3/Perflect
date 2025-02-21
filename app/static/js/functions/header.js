//header.js

document.getElementById('reboot').addEventListener('click', function() {
    if (confirm("Are you sure you want to reboot the system?")) {
        fetch('/reboot_system', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('System rebooting...');
            } else {
                alert('Failed to reboot the system.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while attempting to reboot.');
        });
    }
});