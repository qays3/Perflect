#!/bin/bash

sudo apt install ufw -y 
sudo apt install nginx -y
sudo apt install htop iotop -y
sudo apt install -y docker.io
sudo apt install openvpn -y
sudo apt-get install easy-rsa

dpkg-query -L easy-rsa

cd app

if [ ! -d "myenv" ]; then
    python3 -m venv myenv
fi

source myenv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt

if ! [ -x "$(command -v uvicorn)" ]; then
    pip install uvicorn
fi

sudo nohup ./myenv/bin/uvicorn main:app --reload --host 127.0.0.1 --port 9393 &

echo -e "\033[0;32mVisit the website at http://127.0.0.1:9393\033[0m"
