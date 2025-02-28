<<<<<<< HEAD
import subprocess
from pydantic import BaseModel
from typing import List
import logging
import inspect
import os

log_dir = './logs'
log_file = 'perflect.log'
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, log_file)

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_message(level, message, source):
    caller = inspect.stack()[1].function
    if level == 'info':
        logging.info(f"[{source}] [{caller}] {message}")
    elif level == 'error':
        logging.error(f"[{source}] [{caller}] {message}")
    elif level == 'warning':
        logging.warning(f"[{source}] [{caller}] {message}")

class PortInfo(BaseModel):
    port: int
    service: str
    protocol: str
    pid: int

class PortsData:
    @staticmethod
    def get_ports() -> List[PortInfo]:
        try:
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
            log_message('info', "Fetched open ports", "ports")
            return ports_info
        except subprocess.CalledProcessError as e:
            log_message('error', f"Failed to fetch open ports: {e}", "ports")
            return []

    @staticmethod
    def open_port(port: int) -> None:
        if port < 1024 or port > 65535:
            log_message('error', f"Port {port} is outside the allowed range. Please choose a port between 1024 and 65535.", "ports")
            raise ValueError(f"Port {port} is outside the allowed range. Please choose a port between 1024 and 65535.")
        
        existing_ports = PortsData.get_ports()
        if any(p.port == port for p in existing_ports):
            log_message('error', f"Port {port} is already open.", "ports")
            raise ValueError(f"Port {port} is already open.")

        try:
            subprocess.run(
                ["sudo", "sh", "-c", f"nc -l -p {port} &"],  
                check=True
            )
            log_message('info', f"Port {port} opened successfully.", "ports")
        except subprocess.CalledProcessError as e:
            log_message('error', f"Failed to open port {port}: {e}", "ports")

    @staticmethod
    def close_port(port: int) -> None:
        if port < 1024 or port > 65535:
            log_message('error', f"Port {port} is outside the allowed range. Please choose a port between 1024 and 65535.", "ports")
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
                        log_message('info', f"Port {port} closed successfully.", "ports")
                        return
            log_message('warning', f"Port {port} is not currently open.", "ports")
        except subprocess.CalledProcessError as e:
            log_message('error', f"Failed to close port {port}: {e}", "ports")

    @staticmethod
    def refresh_ports() -> None:
        ports = PortsData.get_ports()
=======
import subprocess
from pydantic import BaseModel
from typing import List
import logging
import inspect
import os

log_dir = './logs'
log_file = 'perflect.log'
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, log_file)

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_message(level, message, source):
    caller = inspect.stack()[1].function
    if level == 'info':
        logging.info(f"[{source}] [{caller}] {message}")
    elif level == 'error':
        logging.error(f"[{source}] [{caller}] {message}")
    elif level == 'warning':
        logging.warning(f"[{source}] [{caller}] {message}")

class PortInfo(BaseModel):
    port: int
    service: str
    protocol: str
    pid: int

class PortsData:
    @staticmethod
    def get_ports() -> List[PortInfo]:
        try:
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
            log_message('info', "Fetched open ports", "ports")
            return ports_info
        except subprocess.CalledProcessError as e:
            log_message('error', f"Failed to fetch open ports: {e}", "ports")
            return []

    @staticmethod
    def open_port(port: int) -> None:
        if port < 1024 or port > 65535:
            log_message('error', f"Port {port} is outside the allowed range. Please choose a port between 1024 and 65535.", "ports")
            raise ValueError(f"Port {port} is outside the allowed range. Please choose a port between 1024 and 65535.")
        
        existing_ports = PortsData.get_ports()
        if any(p.port == port for p in existing_ports):
            log_message('error', f"Port {port} is already open.", "ports")
            raise ValueError(f"Port {port} is already open.")

        try:
            subprocess.run(
                ["sudo", "sh", "-c", f"nc -l -p {port} &"],  
                check=True
            )
            log_message('info', f"Port {port} opened successfully.", "ports")
        except subprocess.CalledProcessError as e:
            log_message('error', f"Failed to open port {port}: {e}", "ports")

    @staticmethod
    def close_port(port: int) -> None:
        if port < 1024 or port > 65535:
            log_message('error', f"Port {port} is outside the allowed range. Please choose a port between 1024 and 65535.", "ports")
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
                        log_message('info', f"Port {port} closed successfully.", "ports")
                        return
            log_message('warning', f"Port {port} is not currently open.", "ports")
        except subprocess.CalledProcessError as e:
            log_message('error', f"Failed to close port {port}: {e}", "ports")

    @staticmethod
    def refresh_ports() -> None:
        ports = PortsData.get_ports()
>>>>>>> 056fad599c7648f2a924f04ea510b355067a52e4
        log_message('info', "Ports refreshed", "ports")