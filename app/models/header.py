import subprocess

def perform_reboot():
    try:
        
        subprocess.run(['sudo', 'reboot'], check=True)
        return {"status": "success", "message": "System is rebooting."}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": "Failed to reboot the system."}
