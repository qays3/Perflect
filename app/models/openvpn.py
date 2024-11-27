import os
import subprocess
import time
from pydantic import BaseModel


class OpenVPNData(BaseModel):
    client_name: str = "client"

    def run_command(self, command, sudo=False, background=False):
        if sudo:
            command = f"sudo {command}"
        
        try:
            start_time = time.time()
            if background:
                result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"Running command '{command}' in the background...")
                return result
            else:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                elapsed_time = time.time() - start_time
                if result.returncode != 0:
                    raise Exception(f"Error running command: {command}\n{result.stderr}")
                print(f"Command '{command}' completed in {elapsed_time:.2f}s")
                return result.stdout.strip()
        except Exception as e:
            print(f"Error in command execution: {e}")
            return None

    def get_server_ip(self):

        command = "hostname -I | awk '{print $1}'"
        ip_address = self.run_command(command)
        if ip_address:
            return ip_address.strip()
        else:
            return "127.0.0.1"  

    def generate_ovpn_file(self):
        print("Generating .ovpn client file...")
        client_ovpn_file = f"/root/{self.client_name}.ovpn"
        
        server_ip = self.get_server_ip() 

        ca_cert_path = "/root/easy-rsa/pki/ca.crt"
        client_cert_path = "/root/easy-rsa/pki/issued/client.crt"
        client_key_path = "/root/easy-rsa/pki/private/client.key"

        try:
            with open(ca_cert_path, "r") as ca_file:
                ca_cert_content = ca_file.read()

            with open(client_cert_path, "r") as client_cert_file:
                client_cert_content = client_cert_file.read()

            with open(client_key_path, "r") as client_key_file:
                client_key_content = client_key_file.read()
        except FileNotFoundError as e:
            print(f"Error reading files: {e}")
            return None

        ovpn_content = f"""
client
dev tun
proto udp
remote {server_ip} 1194
resolv-retry infinite
nobind
persist-key
persist-tun
ca ca.crt
cert client.crt
key client.key
cipher AES-256-CBC
auth SHA256
verb 3

<ca>
{ca_cert_content}
</ca>
<cert>
{client_cert_content}
</cert>
<key>
{client_key_content}
</key>
"""

        with open(client_ovpn_file, "w") as ovpn_file:
            ovpn_file.write(ovpn_content)

        print(f".ovpn client configuration file generated at {client_ovpn_file}")
        return client_ovpn_file
