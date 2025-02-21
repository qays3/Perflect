async function fetchProcesses() {
    const response = await fetch('/processes');
    const data = await response.json();
    const processList = document.getElementById('processList');
    const processRows = Array.from(processList.getElementsByTagName('tr'));

    processRows.forEach(row => {
      const pid = row.id.replace('process-', '');
      if (!data.processes.some(p => p.pid === parseInt(pid))) {
        row.remove();
      }
    });

    data.processes.forEach(process => {
      const existingRow = document.getElementById(`process-${process.pid}`);
      if (!existingRow) {
        const row = document.createElement('tr');
        row.id = `process-${process.pid}`;
        row.className = 'text-sm';
        row.innerHTML = `
          <td class="px-4 py-2">${process.pid}</td>
          <td class="px-4 py-2">${process.name}</td>
          <td class="px-4 py-2">${process.cpu}</td>
          <td class="px-4 py-2">${process.memory}</td>
          <td class="px-4 py-2">
            <button class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition duration-200" onclick="killProcess(${process.pid})">Kill</button>
            <button class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition duration-200 ml-2" onclick="killProcessForce(${process.pid})">Kill Force</button>
          </td>
        `;
        processList.appendChild(row);
      } else {
        existingRow.children[2].textContent = process.cpu;
        existingRow.children[3].textContent = process.memory;
      }
    });
  }

  async function killProcess(pid) {
  const button = document.querySelector(`button[onclick="killProcess(${pid})"]`);
  if (button) {
      button.classList.add("reloading");
      button.style.pointerEvents = "none";
  }

  const response = await fetch(`/kill/${pid}`, { method: 'POST' });
  if (response.ok) {
      removeProcessRow(pid);
      showMessage('Process killed successfully.');
  }

  if (button) {
      button.classList.remove("reloading");
      button.style.pointerEvents = "auto";
  }
}

async function killProcessForce(pid) {
  const button = document.querySelector(`button[onclick="killProcessForce(${pid})"]`);
  if (button) {
      button.classList.add("reloading");
      button.style.pointerEvents = "none";
  }

  const response = await fetch(`/kill_force/${pid}`, { method: 'POST' });
  if (response.ok) {
      removeProcessRow(pid);
      showMessage('Force kill executed.');
  }

  if (button) {
      button.classList.remove("reloading");
      button.style.pointerEvents = "auto";
  }
}

  function removeProcessRow(pid) {
    const row = document.getElementById(`process-${pid}`);
    if (row) {
      row.remove();
    }
  }

  function showMessage(message) {
    const messageBox = document.getElementById('messageBox');
    messageBox.innerText = message;
    messageBox.style.display = 'block';
    setTimeout(() => {
      messageBox.style.display = 'none';
    }, 2000);
  }

  setInterval(fetchProcesses, 5000);
  window.onload = fetchProcesses;