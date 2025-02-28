// docker.js

document.addEventListener("DOMContentLoaded", function () {
    function startReloadAnimation(button) {
        button.classList.add("reloading");
        button.style.pointerEvents = "none";
    }

    function stopReloadAnimation(button) {
        button.classList.remove("reloading");
        button.style.pointerEvents = "auto";
    }

    function attachStopButtonListeners() {
        document.querySelectorAll(".stop-btn").forEach((btn) => {
            btn.addEventListener("click", async function () {
                startReloadAnimation(this);
                const containerId = this.getAttribute("data-id");
                const response = await fetch(`/docker/stop/${containerId}`, { method: "POST" });
                const data = await response.json();
                updateTable(data.containers);
                showMessage(data.message);
                stopReloadAnimation(this);
            });
        });
    }

    const cleanCacheBtn = document.getElementById("cleanCacheBtn");
    cleanCacheBtn.addEventListener("click", async () => {
        startReloadAnimation(cleanCacheBtn);
        const response = await fetch("/docker/clean_cache", { method: "POST" });
        const data = await response.json();
        updateTable(data.containers);
        showMessage(data.message);
        stopReloadAnimation(cleanCacheBtn);
    });

    const stopAllBtn = document.getElementById("stopAllBtn");
    stopAllBtn.addEventListener("click", async () => {
        startReloadAnimation(stopAllBtn);
        const response = await fetch("/docker/stop_all", { method: "POST" });
        const data = await response.json();
        if (data.message) {
            showMessage(data.message);
        } else {
            showMessage("Failed to stop all containers.");
        }
        updateTable(data.containers);
        stopReloadAnimation(stopAllBtn);
    });

    const runContainerBtn = document.getElementById("runContainerBtn");
    runContainerBtn.addEventListener("click", async () => {
        startReloadAnimation(runContainerBtn);
        const image = document.getElementById("dockerImage").value.trim();

        if (!image) {
            showMessage("Image name is required.");
            stopReloadAnimation(runContainerBtn);
            return;
        }

        try {
            const response = await fetch("/docker/run", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ image: image }),
            });

            const data = await response.json();

            if (response.ok) {
                updateTable(data.containers);
                showMessage(data.message);
            } else {
                showMessage(data.error || "Failed to start container.");
            }
        } catch (err) {
            showMessage("An error occurred while communicating with the server.");
        } finally {
            stopReloadAnimation(runContainerBtn);
        }
    });

    function updateTable(containers) {
        const tableBody = document.getElementById("dockerTableBody");
        tableBody.innerHTML = containers
            .map(
                (container) => `
                <tr class="border-b border-gray-200 dark:border-gray-700">
                    <td class="px-4 py-2">${container.container_id}</td>
                    <td class="px-4 py-2">${container.image}</td>
                    <td class="px-4 py-2">${container.command}</td>
                    <td class="px-4 py-2">${container.created}</td>
                    <td class="px-4 py-2">${container.status}</td>
                    <td class="px-4 py-2">${container.ports}</td>
                    <td class="px-4 py-2">${container.names}</td>
                    <td class="px-4 py-2">
                        <button class="stop-btn bg-[#8743ff] text-white py-2 px-4 rounded" data-id="${container.container_id}" style="background-color: #8743ff;">
                            <span class="reload-icon"></span>
                            <span class="button-text">Stop</span>
                        </button>
                    </td>
                </tr>
            `
            )
            .join("");

        attachStopButtonListeners();
    }

    function showMessage(message) {
        const messageBox = document.getElementById("messageBox");
        messageBox.innerText = message;
        messageBox.style.display = "block";
        setTimeout(() => {
            messageBox.style.display = "none";
        }, 3000);
    }

    attachStopButtonListeners();
});