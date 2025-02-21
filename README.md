
## Perflect Dashboard

![alt text](images/Perflect.png)

Perflect Dashboard is a FastAPI-powered application designed to optimize and manage Linux-based operating systems. It provides a range of system utilities and monitoring tools accessible via a web-based dashboard, making it easy to configure, monitor, and control essential aspects of your OS. Key features include Docker management, OpenVPN creation, system controls, automated tasks, and network traffic monitoring, all designed to help streamline Linux server management.

<video controls src="video/Perflect.mp4" title="Title"></video>

---

# Table of Contents

1. [Perflect Dashboard Overview](#Perflect-Dashboard)
2. [Project Structure](#Project-Structure)
3. [Features](#Features)
4. [Pages](#Pages)
   - [Dashboard](#Dashboard)
   - [Analytics](#Analytics)
   - [Ports](#Ports)
   - [Startups](#Startups)
   - [Docker](#Docker)
   - [Processes](#Processes)
   - [OpenVPN](#OpenVPN)
5. [Installation](#Installation)
6. [Contributors](#Contributors)
7. [Credits](#Credits)

---


## Project Structure

```bash
Perflect/
│
├── app/
│   ├── config/
│   │   └── templates.py
│   │
│   ├── controllers/
│   │   ├── analytics.py
│   │   ├── blank.py
│   │   ├── dashboard.py
│   │   ├── docker.py
│   │   ├── header.py
│   │   ├── openvpn.py
│   │   ├── ports.py
│   │   ├── processes.py
│   │   └── startups.py
│   │
│   ├── models/
│   │   ├── analytics.py
│   │   ├── blank.py
│   │   ├── dashboard.py
│   │   ├── docker.py
│   │   ├── header.py
│   │   ├── openvpn.py
│   │   ├── ports.py
│   │   ├── processes.py
│   │   └── startups.py
│   │
│   ├── static/
│   │   ├── css/
│   │   │   ├── main.css
│   │   │   ├── scroll.css
│   │   │   ├── tailwind.css
│   │   │   └── tailwind.output.css
│   │   │
│   │   ├── img/
│   │   │   └── Perflect.png
│   │   │
│   │   └── js/
│   │       ├── charts-bars.js
│   │       ├── charts-lines.js
│   │       ├── charts-pie.js
│   │       ├── focus-trap.js
│   │       ├── init-alpine.js
│   │       └── script.js
│   │
│   ├── templates/
│   │   ├── includes/
│   │   │   ├── header.html
│   │   │   └── sidebar.html
│   │   │
│   │   ├── analytics.html
│   │   ├── blank.html
│   │   ├── dashboard.html
│   │   ├── docker.html
│   │   ├── openvpn.html
│   │   ├── ports.html
│   │   ├── processes.html
│   │   └── startups.html
│   │
│   ├── LICENSE
│   ├── main.py
│   ├── README.md
│   ├── requirements.txt
│   └── setup.sh
│
├── images/
│   └── Perflect.png
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## Features

- **OpenVPN Management**: Configure and manage OpenVPN instances to set up a secure network.
- **Docker Management**: Monitor and control Docker containers directly from the dashboard.
- **Startups**: Configure startup processes.
- **Process Management**: View and manage running processes on the system.
- **Port Monitoring**: Monitor open and closed ports on the server.

---

## Pages

### Dashboard

The main overview page that provides a summary of key system metrics, health indicators, and performance statistics. This acts as the central hub where users can get an at-a-glance view of the server's status.

```py
    def get_data(cls):
        uptime = os.popen("uptime -p").read().strip()
        firewall_status = os.popen("sudo ufw status | grep 'Status:'").read().strip()

        load_avg = os.getloadavg()
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_usage = {
            "current": round(cpu_percent, 1),
            "peak": round(max(load_avg), 1),
            "load": [round(load, 1) for load in load_avg],
        }

        memory = psutil.virtual_memory()
        memory_usage = {
            "total": round(memory.total / (1024 ** 3), 1),
            "used": round(memory.used / (1024 ** 3), 1),
            "free": round(memory.available / (1024 ** 3), 1),
        }

        disk = psutil.disk_usage("/")
        disk_usage = {
            "total": round(disk.total / (1024 ** 3), 1),
            "used": round(disk.used / (1024 ** 3), 1),
            "free": round(disk.free / (1024 ** 3), 1),
        }

        net_io = psutil.net_io_counters()
        network_activity = {
            "inbound": round(net_io.bytes_recv / 1024, 1),
            "outbound": round(net_io.bytes_sent / 1024, 1),
        }
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        data = cls(
            uptime=uptime,
            firewall_status=firewall_status,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            network_activity=network_activity,
            timestamp=timestamp
        )

        cls.store_data(data)

        return data
```

### Analytics

A detailed system analytics page with charts and graphs tracking metrics like CPU usage, memory usage, disk space, and historical performance. This page provides insights into resource utilization trends to help optimize server performance over time.

```py
class AnalyticsData(BaseModel):
    cpu_usage: List[float]
    memory_usage: List[float]
    disk_usage: List[float]
    network_activity: List[float]
    system_load: List[float]
    timestamp: str

    @classmethod
    def get_data(cls):
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_usage = [round(cpu_percent, 1)]

        memory = psutil.virtual_memory()
        memory_usage = [round(memory.used / (1024 ** 3), 1)]

        disk = psutil.disk_usage("/")
        disk_usage = [round(disk.used / (1024 ** 3), 1)]

        net_io = psutil.net_io_counters()
        network_activity = [round(net_io.bytes_recv / 1024, 1)]

        load_avg = os.getloadavg()
        system_load = [round(load_avg[0], 1)]

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        data = cls(
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            network_activity=network_activity,
            system_load=system_load,
            timestamp=timestamp
        )

        cls.store_data(data)

        return data
```

### Ports

A dedicated page for port monitoring, listing all open, closed, and recently active ports. This page helps in identifying potential vulnerabilities or unauthorized access points, aiding in network security management.

```py
    def get_ports() -> List[PortInfo]:
        result = subprocess.run(
            ["sudo", "ss", "-tunap"], capture_output=True, text=True, check=True
        )

        ports_info = []
        for line in result.stdout.splitlines():
            if "LISTEN" in line:
                parts = line.split()
                addr = parts[4]
                pid_info = parts[6] if len(parts) > 6 else ""
                port = addr.split(":")[-1]
                protocol = "TCP" if "tcp" in parts[0] else "UDP"
                service = port if port.isdigit() else "-"
                pid = None
                if "pid=" in pid_info:
                    pid = pid_info.split("=")[1].split(",")[0]
                    pid = int(pid)
                ports_info.append(
                    PortInfo(
                        port=int(port),
                        service=service,
                        protocol=protocol,
                        pid=pid if pid else 0,
                    )
                )
        return ports_info
```

### Startups
The startups page allows users to upload shell scripts or executable files to be added to system startup.

```py
    def add_startup_file(file) -> str:
        filename = file.filename
        file_extension = os.path.splitext(filename)[1]

        if file_extension not in ['.sh', '.bash', '.service']:
            raise ValueError("Invalid file type")

        destination_path =

 os.path.join('/etc/init.d', filename)

        with open(destination_path, 'wb') as f:
            f.write(file.read())

        os.chmod(destination_path, 0o755)

        return f"File {filename} added to startup scripts."
```

---

### Docker

The Docker page allows users to manage Docker containers directly from the dashboard, offering insights into their status and the ability to start, stop, or restart containers.

```py
    def get_docker_containers() -> List[DockerContainer]:
        result = subprocess.run(
            ["docker", "ps", "-a"], capture_output=True, text=True, check=True
        )

        containers = []
        for line in result.stdout.splitlines()[1:]:
            parts = line.split()
            container_id = parts[0]
            container_name = parts[-1]
            status = parts[4]
            containers.append(DockerContainer(id=container_id, name=container_name, status=status))

        return containers
```
---
### Processes

The Processes page provides detailed information about running processes, including the ability to manage them (kill, stop, restart, etc.).

```py
    def get_processes() -> List[ProcessInfo]:
        result = subprocess.run(
            ["ps", "-aux"], capture_output=True, text=True, check=True
        )

        processes = []
        for line in result.stdout.splitlines()[1:]:
            parts = line.split()
            pid = parts[1]
            user = parts[0]
            cpu = parts[2]
            mem = parts[3]
            command = " ".join(parts[10:])
            processes.append(ProcessInfo(pid=pid, user=user, cpu=cpu, mem=mem, command=command))

        return processes
```
---
### OpenVPN

The OpenVPN page enables the creation and management of OpenVPN instances to establish secure connections.

```py
    def create_openvpn_config(file) -> str:
        filename = file.filename
        destination_path = os.path.join("/etc/openvpn", filename)

        with open(destination_path, 'wb') as f:
            f.write(file.read())

        subprocess.run(["systemctl", "start", "openvpn@{}".format(filename)], check=True)
        return f"OpenVPN instance {filename} created and started."
```

---



## Installation

```bash
git clone https://github.com/your-repository/perflect-dashboard.git
cd perflect-dashboard
pip install -r requirements.txt
```

Run the app:

```bash
uvicorn app.main:app --reload
```

---

## Contributors

<div style="display: flex; align-items: center; margin-bottom: 20px;">
    <a href="https://github.com/qays3" style="text-decoration: none; display: flex; align-items: center;">
        <img src="https://github.com/qays3.png" alt="@qays3" title="@qays3" width="100px" height="100px" style="border-radius: 50%; margin-right: 10px;">
    </a>
</div>

## Credits

[qays3](https://github.com/qays3) ([Support qays](https://buymeacoffee.com/hidden))