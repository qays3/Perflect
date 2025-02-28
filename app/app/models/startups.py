<<<<<<< HEAD
import shutil
import os
import subprocess
import logging
import inspect

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

class StartupsData:
    @staticmethod
    def add_startup_file(file) -> str:
        try:
            filename = file.filename
            file_extension = os.path.splitext(filename)[1]

            if file_extension not in ['.sh', '.bash', '.service']:
                log_message('error', f"Invalid file type: {file_extension}", "startup")
                raise ValueError("Invalid file type")

            destination_path = f"/etc/init.d/{filename}"

            with open(destination_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            os.chmod(destination_path, 0o755)

            if file_extension == '.service':
                subprocess.run(f"sudo systemctl daemon-reload", shell=True, check=True)
                subprocess.run(f"sudo systemctl start {filename}", shell=True, check=True)

            log_message('info', f"File {filename} added to startup successfully", "startup")
            return f"File {filename} added to startup successfully"
        except ValueError as ve:
            log_message('error', str(ve), "startup")
            return str(ve)
        except Exception as e:
            log_message('error', f"Failed to add file {filename} to startup: {e}", "startup")
=======
import shutil
import os
import subprocess
import logging
import inspect

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

class StartupsData:
    @staticmethod
    def add_startup_file(file) -> str:
        try:
            filename = file.filename
            file_extension = os.path.splitext(filename)[1]

            if file_extension not in ['.sh', '.bash', '.service']:
                log_message('error', f"Invalid file type: {file_extension}", "startup")
                raise ValueError("Invalid file type")

            destination_path = f"/etc/init.d/{filename}"

            with open(destination_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            os.chmod(destination_path, 0o755)

            if file_extension == '.service':
                subprocess.run(f"sudo systemctl daemon-reload", shell=True, check=True)
                subprocess.run(f"sudo systemctl start {filename}", shell=True, check=True)

            log_message('info', f"File {filename} added to startup successfully", "startup")
            return f"File {filename} added to startup successfully"
        except ValueError as ve:
            log_message('error', str(ve), "startup")
            return str(ve)
        except Exception as e:
            log_message('error', f"Failed to add file {filename} to startup: {e}", "startup")
>>>>>>> 056fad599c7648f2a924f04ea510b355067a52e4
            return f"Failed to add file {filename} to startup: {e}"