import subprocess
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

def perform_reboot():
    try:
        subprocess.run(['sudo', 'reboot'], check=True)
        log_message('info', "System is rebooting", "reboot")
        return {"status": "success", "message": "System is rebooting."}
    except subprocess.CalledProcessError as e:
        log_message('error', f"Failed to reboot the system: {e}", "reboot")
        return {"status": "error", "message": "Failed to reboot the system."}