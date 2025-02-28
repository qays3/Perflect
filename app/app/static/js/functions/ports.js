// ports.js


function startReloadAnimation(button) {
    button.classList.add("reloading");
    button.style.pointerEvents = "none";
}

function stopReloadAnimation(button) {
    button.classList.remove("reloading");
    button.style.pointerEvents = "auto";
}

function handlePort(action) {
    const port = document.getElementById("portNumber").value;

    if (!port) {
        alert("Please enter a port number.");
        return;
    }

    const button = action === "close" 
        ? document.querySelector(`button[onclick="handleClosePort(${port})"]`) 
        : document.querySelector(`button[onclick="handlePort('${action}')"]`);

    if (button) {
        startReloadAnimation(button);
    }

    const url = action === "close" ? `/ports/close/${port}` : `/ports/open/${port}`;

    fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                alert("Error: " + (data.detail || "Unknown error"));
            });
        }
        return response.json();
    })
    .then(data => {
        if (data && data.status) {
            alert(data.status);
            updatePortsTable(data.ports);
        }
    })
    .catch(error => {
        alert("Network error: " + error);
    })
    .finally(() => {
        if (button) {
            stopReloadAnimation(button);
        }
    });
}

function handleClosePort(port) {
    const button = document.querySelector(`button[onclick="handleClosePort(${port})"]`);

    if (button) {
        startReloadAnimation(button);
    }

    fetch(`/ports/close/${port}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
    })
    .then(response => response.json())
    .then(data => {
        if (data && data.status) {
            alert(data.status);
            updatePortsTable(data.ports);
        }
    })
    .catch(error => alert("Error: " + error))
    .finally(() => {
        if (button) {
            stopReloadAnimation(button);
        }
    });
}

function updatePortsTable(ports) {
    const tableBody = document.getElementById("portsTableBody");
    tableBody.innerHTML = '';
    ports.forEach(port => {
        const row = document.createElement("tr");
        row.classList.add("border-b", "dark:border-gray-700", "text-gray-800", "dark:text-gray-300");
        row.innerHTML = `
            <td class="px-4 py-2">${port.port}</td>
            <td class="px-4 py-2">${port.service}</td>
            <td class="px-4 py-2">${port.protocol}</td>
            <td class="px-4 py-2">${port.pid}</td>
            <td class="px-4 py-2">
                <button onclick="handleClosePort(${port.port})" class="px-4 py-2 text-white rounded-md" style="background-color: #8743ff;">
                    <span class="reload-icon"></span>
                    <span class="button-text">Close</span>
                </button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}