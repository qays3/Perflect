from pydantic import BaseModel
from typing import List
import psutil


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
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            processes.append(
                ProcessData(
                    pid=proc.info['pid'],
                    name=proc.info['name'],
                    cpu=f"{proc.info['cpu_percent']}%",
                    memory=f"{proc.info['memory_percent']}%"
                )
            )
        return ProcessesData(processes=processes)

    @staticmethod
    def kill_process(pid: int) -> str:
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            proc.wait(timeout=3)
            return "Process killed successfully."
        except psutil.NoSuchProcess:
            return "Process not found."
        except Exception as e:
            return str(e)

    @staticmethod
    def kill_process_force(pid: int) -> str:
        try:
            proc = psutil.Process(pid)
            proc.kill()
            return "Process forcefully killed."
        except psutil.NoSuchProcess:
            return "Process not found."
        except Exception as e:
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
            return None
        except Exception as e:
            return None
