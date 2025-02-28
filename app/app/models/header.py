import subprocess
import logging
import inspect
import os
<<<<<<< HEAD
import psutil
from collections import deque
=======
>>>>>>> 056fad599c7648f2a924f04ea510b355067a52e4

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

def perform_reboot():
    try:
        subprocess.run(['sudo', 'reboot'], check=True)
        log_message('info', "System is rebooting", "reboot")
        return {"status": "success", "message": "System is rebooting."}
    except subprocess.CalledProcessError as e:
        log_message('error', f"Failed to reboot the system: {e}", "reboot")
<<<<<<< HEAD
        return {"status": "error", "message": "Failed to reboot the system."}

cpu_history = deque(maxlen=30)
ram_history = deque(maxlen=30)

def get_resources_usage():
    cpu_usage = 0
    ram_usage = 0

    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_info']):
        cmdline = proc.info['cmdline']
        if cmdline and 'uvicorn' in cmdline and 'main:app' in cmdline:
            cpu_usage = proc.cpu_percent(interval=1) / psutil.cpu_count(logical=True)
            
            total_ram = psutil.virtual_memory().total
            ram_usage = (proc.info['memory_info'].rss / total_ram) * 100
            break

    cpu_history.append(cpu_usage)
    ram_history.append(ram_usage)

    return cpu_usage, ram_usage

def get_resources_history():
    return list(cpu_history), list(ram_history)
=======
        return {"status": "error", "message": "Failed to reboot the system."}
>>>>>>> 056fad599c7648f2a924f04ea510b355067a52e4
