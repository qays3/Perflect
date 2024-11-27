from pydantic import BaseModel
import subprocess
from typing import List
import re


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
        result = subprocess.run(command, capture_output=True, text=True)
        containers = []

        if result.returncode == 0:
            for line in result.stdout.splitlines():
                parts = line.split(",", 6)
                if len(parts) == 7:
                    containers.append(
                        DockerContainer(
                            container_id=parts[0].strip(),
                            image=parts[1].strip(),
                            command=parts[2].strip(),
                            created=parts[3].strip(),
                            status=parts[4].strip(),
                            ports=parts[5].strip(),
                            names=parts[6].strip(),
                        )
                    )
        return containers

    @staticmethod
    def stop_container(container_id: str) -> str:
        if not container_id.isalnum():
            return "Invalid container ID."
        command = ["sudo", "docker", "stop", container_id]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return f"Container {container_id} stopped successfully."
        return f"Failed to stop container {container_id}."

    @staticmethod
    def clean_cache() -> str:
        command = ["docker", "system", "prune", "-a", "-f"]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return "Docker cache cleaned successfully."
        return "Failed to clean Docker cache."

    @staticmethod
    def stop_all_containers() -> str:
        command = ["docker", "stop", "$(docker ps -a -q)"]
        result = subprocess.run(command, capture_output=True, text=True, shell=False)
        if result.returncode == 0:
            return "All containers stopped successfully."
        return f"Failed to stop all containers: {result.stderr.strip()}"

    @staticmethod
    def run_container_with_command(command: str) -> str:
        allowed_commands = ["docker", "run"]
        if not command.split()[0] in allowed_commands:
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
                    return f"Container using port {port} is already running."

        command_args = command.split()
        result = subprocess.run(command_args, capture_output=True, text=True)

        if result.returncode == 0:
            return "Container started successfully."
        return f"Failed to start container: {result.stderr.strip()}"
