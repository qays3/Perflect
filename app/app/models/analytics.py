import json
import psutil
import os
from datetime import datetime
from pydantic import BaseModel
from typing import List
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

class AnalyticsData(BaseModel):
    cpu_usage: List[float]
    memory_usage: List[float]
    disk_usage: List[float]
    network_activity: List[float]
    system_load: List[float]
    timestamp: str

    @classmethod
    def get_data(cls):
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_usage = [round(cpu_percent, 1)]

        memory = psutil.virtual_memory()
        memory_usage = [round(memory.used / (1024 ** 3), 1)]

        disk = psutil.disk_usage("/")
        disk_usage = [round(disk.used / (1024 ** 3), 1)]

        net_io = psutil.net_io_counters()
        network_activity = [round(net_io.bytes_recv / 1024, 1)]

        load_avg = os.getloadavg()
        system_load = [round(load_avg[0], 1)]

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        data = cls(
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            network_activity=network_activity,
            system_load=system_load,
            timestamp=timestamp
        )

        cls.store_data(data)

        return data

    @classmethod
    def store_data(cls, data: 'AnalyticsData'):
        try:
            file_dir = 'json'
            file_path = os.path.join(file_dir, 'analytics.json')

            if not os.path.exists(file_dir):
                os.makedirs(file_dir)

            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    all_data = json.load(f)
            else:
                all_data = []

            all_data.append(data.dict())

            if len(all_data) > 60:
                all_data = all_data[-60:]

            with open(file_path, 'w') as f:
                json.dump(all_data, f, indent=4)

            log_message('info', "Data stored successfully", "analytics")

        except Exception as e:
            log_message('error', f"Error storing data: {e}", "analytics")

    @classmethod
    def get_historical_data(cls):
        try:
            file_path = 'json/analytics.json'
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
            else:
                log_message('warning', "No historical data found", "analytics")
                return []
        except Exception as e:
            log_message('error', f"Error reading data: {e}", "analytics")
            return []