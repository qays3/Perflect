import subprocess
from pydantic import BaseModel
from typing import List


class PortInfo(BaseModel):
    port: int
    service: str
    protocol: str
    pid: int


class PortsData:

    @staticmethod
    def get_ports() -> List[PortInfo]:
        result = subprocess.run(
            ["sudo", "ss", "-tunap"], capture_output=True, text=True, check=True
        )
        ports_info = []
        for line in result.stdout.splitlines():
            if "LISTEN" in line:
                parts = line.split()
                addr = parts[4]
                pid_info = parts[6] if len(parts) > 6 else ''
                port = addr.split(":")[-1]
                protocol = "TCP" if "tcp" in parts[0] else "UDP"
                service = port if port.isdigit() else "-"
                pid = None
                if "pid=" in pid_info:
                    pid = pid_info.split('=')[1].split(',')[0]
                    pid = int(pid)
                ports_info.append(PortInfo(
                    port=int(port),
                    service=service,
                    protocol=protocol,
                    pid=pid if pid else 0
                ))
        return ports_info

    @staticmethod
    def open_port(port: int) -> None:
        if port < 1024 or port > 65535:
            raise ValueError(f"Port {port} is outside the allowed range. Please choose a port between 1024 and 65535.")
        
        existing_ports = PortsData.get_ports()
        if any(p.port == port for p in existing_ports):
            raise ValueError(f"Port {port} is already open.")

        try:
            subprocess.run(
                ["sudo", "sh", "-c", f"nc -l -p {port} &"],  
                check=True
            )
            print(f"Port {port} opened successfully.")
            PortsData.refresh_ports()
        except subprocess.CalledProcessError as e:
            print(f"Failed to open port {port}: {e}")
            print(f"Error details: {e.stderr}")

    @staticmethod
    def close_port(port: int) -> None:
        if port < 1024 or port > 65535:
            raise ValueError(f"Port {port} is outside the allowed range. Please choose a port between 1024 and 65535.")
        try:
            pid_result = subprocess.run(
                ["sudo", "ss", "-tunap"], capture_output=True, text=True
            ).stdout.splitlines()

            for line in pid_result:
                if f":{port}" in line and "LISTEN" in line:
                    pid_info = line.split()[6]
                    if "pid=" in pid_info:
                        pid = pid_info.split('=')[1].split(',')[0]
                        subprocess.run(
                            ["sudo", "kill", "-9", pid],
                            check=True
                        )
                        print(f"Port {port} closed successfully.")
                        PortsData.refresh_ports()
                        return
            print(f"Port {port} is not currently open.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to close port {port}: {e}")

    @staticmethod
    def refresh_ports() -> None:
        ports = PortsData.get_ports()
        print(f"Ports table updated. Current ports: {ports}")
