#!/bin/bash

PORT=9393
IP="127.0.0.1"

setup() {
    sudo apt install ufw -y
    echo ""
    sudo apt install nginx -y
    echo ""
    sudo apt install htop iotop -y
    echo ""
    sudo apt install -y docker.io
    echo ""
    sudo apt install openvpn -y
    echo ""
    sudo apt-get install easy-rsa
    echo ""

    dpkg-query -L easy-rsa

    cd app

    if [ ! -d "myenv" ]; then
        python3 -m venv myenv
    fi

    source myenv/bin/activate

    pip install --upgrade pip
    echo ""
    pip install -r requirements.txt
    echo ""

    if ! [ -x "$(command -v uvicorn)" ]; then
        pip install uvicorn
        echo ""
    fi
}

check_port_running() {
    if lsof -i :$PORT; then
        echo "A process is already using port $PORT."
        read -p "Do you want to stop this process and continue? (y/n): " stop_response
        if [[ "$stop_response" =~ ^[Yy]$ ]]; then
            sudo fuser -k $PORT/tcp
            echo -e "\033[0;32mProcess on port $PORT has been killed.\033[0m"
        else
            echo -e "\033[0;31mThe process on port $PORT will not be stopped. Exiting setup.\033[0m"
            exit 1
        fi
    fi
}

check_startup() {
    if systemctl is-enabled --quiet perflect_dashboard.service; then
        echo "Perflect Dashboard is already set to start on boot."
        read -p "Do you want to remove it from startup? (y/n): " remove_response
        if [[ "$remove_response" =~ ^[Yy]$ ]]; then
            sudo systemctl disable perflect_dashboard.service
            sudo systemctl stop perflect_dashboard.service
            echo -e "\033[0;32mPerflect Dashboard has been removed from startup.\033[0m"
        fi
    else
        echo "Perflect Dashboard is not set to start on boot."
        read -p "Do you want to add it to startup? (y/n): " add_response
        if [[ "$add_response" =~ ^[Yy]$ ]]; then
            echo -e "[Unit]
Description=Perflect Dashboard
After=network.target

[Service]
User=$USER
WorkingDirectory=$PWD/app
ExecStart=$PWD/app/myenv/bin/uvicorn main:app --reload --host $IP --port $PORT
Restart=always

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/perflect_dashboard.service > /dev/null

            sudo systemctl daemon-reload
            sudo systemctl enable perflect_dashboard.service
            sudo systemctl start perflect_dashboard.service

            echo -e "\033[0;32mPerflect Dashboard has been set to start automatically on boot.\033[0m"
        fi
    fi
}

start_application() {
    sudo nohup ./myenv/bin/uvicorn main:app --reload --host $IP --port $PORT > /dev/null 2>&1 &
    echo -e "\033[0;32mVisit the website at http://$IP:$PORT\033[0m"
}

main() {
    setup
    check_port_running
    check_startup
    start_application
}

main
