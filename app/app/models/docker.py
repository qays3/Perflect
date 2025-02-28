<<<<<<< HEAD
from pydantic import BaseModel
import subprocess
from typing import List
import re
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

class DockerContainer(BaseModel):
    container_id: str
    image: str
    command: str
    created: str
    status: str
    ports: str
    names: str

class DockerOperations:
    @staticmethod
    def get_running_containers() -> List[DockerContainer]:
        command = [
            "docker",
            "ps",
            "--format",
            "{{.ID}},{{.Image}},{{.Command}},{{.CreatedAt}},{{.Status}},{{.Ports}},{{.Names}}",
        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            containers = []
            for line in result.stdout.splitlines():
                parts = line.split(",", 6)
                if len(parts) == 7:
                    ports = parts[5].strip()
                    names = parts[6].strip()
                    if "," in names:
                        names = names.split(",")[-1].strip()
                    containers.append(
                        DockerContainer(
                            container_id=parts[0].strip(),
                            image=parts[1].strip(),
                            command=parts[2].strip(),
                            created=parts[3].strip(),
                            status=parts[4].strip(),
                            ports=ports,
                            names=names,
                        )
                    )
            log_message('info', "Fetched running containers", "docker")
            return containers
        except subprocess.CalledProcessError as e:
            log_message('error', f"Failed to fetch running containers: {e}", "docker")
            return []

    @staticmethod
    def stop_container(container_id: str) -> str:
        if not container_id.isalnum():
            log_message('error', f"Invalid container ID: {container_id}", "docker")
            return "Invalid container ID."
        command = ["docker", "stop", container_id]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            log_message('info', f"Container {container_id} stopped successfully", "docker")
            return f"Container {container_id} stopped successfully."
        except subprocess.CalledProcessError as e:
            log_message('error', f"Failed to stop container {container_id}: {e}", "docker")
            return f"Failed to stop container {container_id}: {e}"

    @staticmethod
    def clean_cache() -> str:
        command = ["docker", "system", "prune", "-a", "-f"]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            log_message('info', "Docker cache cleaned successfully", "docker")
            return "Docker cache cleaned successfully."
        except subprocess.CalledProcessError as e:
            log_message('error', f"Failed to clean Docker cache: {e}", "docker")
            return f"Failed to clean Docker cache: {e}"

    @staticmethod
    def stop_all_containers() -> str:
        get_ids_command = ["docker", "ps", "-a", "-q"]
        try:
            result = subprocess.run(get_ids_command, capture_output=True, text=True, check=True)
            container_ids = result.stdout.splitlines()
            if not container_ids:
                log_message('info', "No containers to stop", "docker")
                return "No containers to stop."
            stop_command = ["docker", "stop"] + container_ids
            result = subprocess.run(stop_command, capture_output=True, text=True, check=True)
            log_message('info', "All containers stopped successfully", "docker")
            return "All containers stopped successfully."
        except subprocess.CalledProcessError as e:
            log_message('error', f"Failed to stop all containers: {e}", "docker")
            return f"Failed to stop all containers: {e}"

    @staticmethod
    def run_container_with_command(command: str) -> str:
        allowed_commands = ["docker", "run"]
        if not command.split()[0] in allowed_commands:
            log_message('error', "Invalid command", "docker")
            return "Invalid command."
        port_match = re.search(r'-p\s*(\d+):\d+', command)
        if port_match:
            port = port_match.group(1)
        else:
            port = None
        if port:
            running_containers = DockerOperations.get_running_containers()
            for container in running_containers:
                if port in container.ports:
                    log_message('error', f"Container using port {port} is already running", "docker")
                    return f"Container using port {port} is already running."
        command_args = command.split()
        try:
            result = subprocess.run(command_args, capture_output=True, text=True, check=True)
            log_message('info', "Container started successfully", "docker")
            return "Container started successfully."
        except subprocess.CalledProcessError as e:
            log_message('error', f"Failed to start container: {e}", "docker")
=======
from pydantic import BaseModel
import subprocess
from typing import List
import re
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

class DockerContainer(BaseModel):
    container_id: str
    image: str
    command: str
    created: str
    status: str
    ports: str
    names: str

class DockerOperations:
    @staticmethod
    def get_running_containers() -> List[DockerContainer]:
        command = [
            "docker",
            "ps",
            "--format",
            "{{.ID}},{{.Image}},{{.Command}},{{.CreatedAt}},{{.Status}},{{.Ports}},{{.Names}}",
        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            containers = []
            for line in result.stdout.splitlines():
                parts = line.split(",", 6)
                if len(parts) == 7:
                    ports = parts[5].strip()
                    names = parts[6].strip()
                    if "," in names:
                        names = names.split(",")[-1].strip()
                    containers.append(
                        DockerContainer(
                            container_id=parts[0].strip(),
                            image=parts[1].strip(),
                            command=parts[2].strip(),
                            created=parts[3].strip(),
                            status=parts[4].strip(),
                            ports=ports,
                            names=names,
                        )
                    )
            log_message('info', "Fetched running containers", "docker")
            return containers
        except subprocess.CalledProcessError as e:
            log_message('error', f"Failed to fetch running containers: {e}", "docker")
            return []

    @staticmethod
    def stop_container(container_id: str) -> str:
        if not container_id.isalnum():
            log_message('error', f"Invalid container ID: {container_id}", "docker")
            return "Invalid container ID."
        command = ["docker", "stop", container_id]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            log_message('info', f"Container {container_id} stopped successfully", "docker")
            return f"Container {container_id} stopped successfully."
        except subprocess.CalledProcessError as e:
            log_message('error', f"Failed to stop container {container_id}: {e}", "docker")
            return f"Failed to stop container {container_id}: {e}"

    @staticmethod
    def clean_cache() -> str:
        command = ["docker", "system", "prune", "-a", "-f"]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            log_message('info', "Docker cache cleaned successfully", "docker")
            return "Docker cache cleaned successfully."
        except subprocess.CalledProcessError as e:
            log_message('error', f"Failed to clean Docker cache: {e}", "docker")
            return f"Failed to clean Docker cache: {e}"

    @staticmethod
    def stop_all_containers() -> str:
        get_ids_command = ["docker", "ps", "-a", "-q"]
        try:
            result = subprocess.run(get_ids_command, capture_output=True, text=True, check=True)
            container_ids = result.stdout.splitlines()
            if not container_ids:
                log_message('info', "No containers to stop", "docker")
                return "No containers to stop."
            stop_command = ["docker", "stop"] + container_ids
            result = subprocess.run(stop_command, capture_output=True, text=True, check=True)
            log_message('info', "All containers stopped successfully", "docker")
            return "All containers stopped successfully."
        except subprocess.CalledProcessError as e:
            log_message('error', f"Failed to stop all containers: {e}", "docker")
            return f"Failed to stop all containers: {e}"

    @staticmethod
    def run_container_with_command(command: str) -> str:
        allowed_commands = ["docker", "run"]
        if not command.split()[0] in allowed_commands:
            log_message('error', "Invalid command", "docker")
            return "Invalid command."
        port_match = re.search(r'-p\s*(\d+):\d+', command)
        if port_match:
            port = port_match.group(1)
        else:
            port = None
        if port:
            running_containers = DockerOperations.get_running_containers()
            for container in running_containers:
                if port in container.ports:
                    log_message('error', f"Container using port {port} is already running", "docker")
                    return f"Container using port {port} is already running."
        command_args = command.split()
        try:
            result = subprocess.run(command_args, capture_output=True, text=True, check=True)
            log_message('info', "Container started successfully", "docker")
            return "Container started successfully."
        except subprocess.CalledProcessError as e:
            log_message('error', f"Failed to start container: {e}", "docker")
>>>>>>> 056fad599c7648f2a924f04ea510b355067a52e4
            return f"Failed to start container: {e}"