<<<<<<< HEAD
from pydantic import BaseModel
from typing import List
import psutil
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

class ProcessData(BaseModel):
    pid: int
    name: str
    cpu: str
    memory: str

class ProcessesData(BaseModel):
    processes: List[ProcessData]

class ProcessManagement:
    @staticmethod
    def get_processes() -> ProcessesData:
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                processes.append(
                    ProcessData(
                        pid=proc.info['pid'],
                        name=proc.info['name'],
                        cpu=f"{proc.info['cpu_percent']}%",
                        memory=f"{proc.info['memory_percent']}%"
                    )
                )
            log_message('info', "Fetched all processes", "processes")
        except Exception as e:
            log_message('error', f"Failed to fetch processes: {e}", "processes")
        return ProcessesData(processes=processes)

    @staticmethod
    def kill_process(pid: int) -> str:
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            proc.wait(timeout=3)
            log_message('info', f"Process {pid} killed successfully", "processes")
            return "Process killed successfully."
        except psutil.NoSuchProcess:
            log_message('error', f"Process {pid} not found", "processes")
            return "Process not found."
        except psutil.TimeoutExpired:
            log_message('error', f"Process {pid} did not terminate within timeout", "processes")
            return "Process did not terminate within timeout."
        except Exception as e:
            log_message('error', f"Failed to kill process {pid}: {e}", "processes")
            return str(e)

    @staticmethod
    def kill_process_force(pid: int) -> str:
        try:
            proc = psutil.Process(pid)
            proc.kill()
            log_message('info', f"Process {pid} forcefully killed", "processes")
            return "Process forcefully killed."
        except psutil.NoSuchProcess:
            log_message('error', f"Process {pid} not found", "processes")
            return "Process not found."
        except Exception as e:
            log_message('error', f"Failed to forcefully kill process {pid}: {e}", "processes")
            return str(e)

    @staticmethod
    def get_process_by_pid(pid: int) -> ProcessData:
        try:
            proc = psutil.Process(pid)
            return ProcessData(
                pid=proc.info['pid'],
                name=proc.info['name'],
                cpu=f"{proc.info['cpu_percent']}%",
                memory=f"{proc.info['memory_percent']}%"
            )
        except psutil.NoSuchProcess:
            log_message('warning', f"Process {pid} not found", "processes")
            return None
        except Exception as e:
            log_message('error', f"Failed to get process {pid}: {e}", "processes")
=======
from pydantic import BaseModel
from typing import List
import psutil
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

class ProcessData(BaseModel):
    pid: int
    name: str
    cpu: str
    memory: str

class ProcessesData(BaseModel):
    processes: List[ProcessData]

class ProcessManagement:
    @staticmethod
    def get_processes() -> ProcessesData:
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                processes.append(
                    ProcessData(
                        pid=proc.info['pid'],
                        name=proc.info['name'],
                        cpu=f"{proc.info['cpu_percent']}%",
                        memory=f"{proc.info['memory_percent']}%"
                    )
                )
            log_message('info', "Fetched all processes", "processes")
        except Exception as e:
            log_message('error', f"Failed to fetch processes: {e}", "processes")
        return ProcessesData(processes=processes)

    @staticmethod
    def kill_process(pid: int) -> str:
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            proc.wait(timeout=3)
            log_message('info', f"Process {pid} killed successfully", "processes")
            return "Process killed successfully."
        except psutil.NoSuchProcess:
            log_message('error', f"Process {pid} not found", "processes")
            return "Process not found."
        except psutil.TimeoutExpired:
            log_message('error', f"Process {pid} did not terminate within timeout", "processes")
            return "Process did not terminate within timeout."
        except Exception as e:
            log_message('error', f"Failed to kill process {pid}: {e}", "processes")
            return str(e)

    @staticmethod
    def kill_process_force(pid: int) -> str:
        try:
            proc = psutil.Process(pid)
            proc.kill()
            log_message('info', f"Process {pid} forcefully killed", "processes")
            return "Process forcefully killed."
        except psutil.NoSuchProcess:
            log_message('error', f"Process {pid} not found", "processes")
            return "Process not found."
        except Exception as e:
            log_message('error', f"Failed to forcefully kill process {pid}: {e}", "processes")
            return str(e)

    @staticmethod
    def get_process_by_pid(pid: int) -> ProcessData:
        try:
            proc = psutil.Process(pid)
            return ProcessData(
                pid=proc.info['pid'],
                name=proc.info['name'],
                cpu=f"{proc.info['cpu_percent']}%",
                memory=f"{proc.info['memory_percent']}%"
            )
        except psutil.NoSuchProcess:
            log_message('warning', f"Process {pid} not found", "processes")
            return None
        except Exception as e:
            log_message('error', f"Failed to get process {pid}: {e}", "processes")
>>>>>>> 056fad599c7648f2a924f04ea510b355067a52e4
            return None