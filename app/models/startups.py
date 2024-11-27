import shutil
import os
import subprocess

class StartupsData:
    
    @staticmethod
    def add_startup_file(file) -> str:
        filename = file.filename
        file_extension = os.path.splitext(filename)[1]

        if file_extension not in ['.sh', '.bash', '.service']:
            raise ValueError("Invalid file type")

        destination_path = f"/etc/init.d/{filename}"

        with open(destination_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        os.chmod(destination_path, 0o755)

        if file_extension == '.service':
            subprocess.run(f"sudo systemctl daemon-reload", shell=True, check=True)
            subprocess.run(f"sudo systemctl start {filename}", shell=True, check=True)

        return f"File {filename} added to startup successfully"
