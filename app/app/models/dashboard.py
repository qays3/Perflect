<<<<<<< HEAD
import json
import psutil
import os
from datetime import datetime
from pydantic import BaseModel
from typing import Dict
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

class DashboardData(BaseModel):
    uptime: str
    firewall_status: str
    cpu_usage: dict
    memory_usage: dict
    disk_usage: dict
    network_activity: dict
    timestamp: str   

    @classmethod
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

    @classmethod
    def store_data(cls, data: 'DashboardData'):
        try:
            file_dir = 'json'
            file_path = os.path.join(file_dir, 'dashboard.json')
            
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    all_data = json.load(f)
            else:
                all_data = []
            
            all_data.append(data.dict())

             
            if len(all_data) > 100:
                all_data = all_data[-100:]

            with open(file_path, 'w') as f:
                json.dump(all_data, f, indent=4)

            log_message('info', "Data stored successfully", "dashboard")

        except Exception as e:
            log_message('error', f"Error storing data: {e}", "dashboard")

    @classmethod
    def get_historical_data(cls):
        try:
            file_path = 'json/dashboard.json'
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
            else:
                log_message('warning', "No historical data found", "dashboard")
                return []
        except Exception as e:
            log_message('error', f"Error reading data: {e}", "dashboard")
=======
import json
import psutil
import os
from datetime import datetime
from pydantic import BaseModel
from typing import Dict
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

class DashboardData(BaseModel):
    uptime: str
    firewall_status: str
    cpu_usage: dict
    memory_usage: dict
    disk_usage: dict
    network_activity: dict
    timestamp: str   

    @classmethod
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

    @classmethod
    def store_data(cls, data: 'DashboardData'):
        try:
            file_dir = 'json'
            file_path = os.path.join(file_dir, 'dashboard.json')
            
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    all_data = json.load(f)
            else:
                all_data = []
            
            all_data.append(data.dict())

             
            if len(all_data) > 100:
                all_data = all_data[-100:]

            with open(file_path, 'w') as f:
                json.dump(all_data, f, indent=4)

            log_message('info', "Data stored successfully", "dashboard")

        except Exception as e:
            log_message('error', f"Error storing data: {e}", "dashboard")

    @classmethod
    def get_historical_data(cls):
        try:
            file_path = 'json/dashboard.json'
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
            else:
                log_message('warning', "No historical data found", "dashboard")
                return []
        except Exception as e:
            log_message('error', f"Error reading data: {e}", "dashboard")
>>>>>>> 056fad599c7648f2a924f04ea510b355067a52e4
            return []