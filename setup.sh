#!/bin/bash

INI="./app/setup.ini"
CONFIG_FILE="$INI"

load_config() {
    if [ -f "$INI" ]; then
        source "$INI"
    else
        PORT=9393
        IP="127.0.0.1"
        STARTUP_ADDED=false
        FLAG=false
    fi
}

check_config() {
    if [ -f "$CONFIG_FILE" ]; then
        source "$CONFIG_FILE"
    else
        PORT=9393
        IP="127.0.0.1"
        STARTUP_ADDED=false
        FLAG=false
    fi
}

save_config() {
    {
        echo ""
        echo "PORT=$PORT"
        echo "IP=$IP"
        echo "STARTUP_ADDED=$STARTUP_ADDED"
        echo "START_TIME=\"$(date '+%Y-%m-%d %H:%M:%S')\""
        echo "FLAG=true"
    } >> "$INI"
}

validate_port() {
    if [[ "$1" =~ ^[0-9]+$ ]] && [ "$1" -ge 1 ] && [ "$1" -le 65535 ]; then
        return 0
    else
        echo -e "\033[0;31mInvalid port number. Port must be a number between 1 and 65535.\033[0m"
        return 1
    fi
}

validate_ip() {
    if [[ "$1" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]]; then
        IFS='.' read -r -a octets <<< "$1"
        for octet in "${octets[@]}"; do
            if [ "$octet" -lt 0 ] || [ "$octet" -gt 255 ]; then
                echo -e "\033[0;31mInvalid IP address. Each octet must be between 0 and 255.\033[0m"
                return 1
            fi
        done
        return 0
    else
        echo -e "\033[0;31mInvalid IP address format. Please use the format xxx.xxx.xxx.xxx.\033[0m"
        return 1
    fi
}

check_port_availability() {
    if lsof -i :$1 > /dev/null 2>&1; then
        echo -e "\033[0;31mPort $1 is already in use. Please choose another port.\033[0m"
        return 1
    else
        return 0
    fi
}

setup() {
    sudo apt-get update
    sudo apt-get install -y python3.12-venv ufw nginx htop iotop docker.io openvpn easy-rsa
    dpkg-query -L easy-rsa > /dev/null 2>&1
    cd "app"
    if [ ! -d "myenv" ]; then
        python3 -m venv myenv
    fi
    source myenv/bin/activate
    pip install --upgrade pip 
    pip install "bleach>=6.0.0" 
    pip install -r requirements.txt 
    if ! pip show uvicorn > /dev/null 2>&1; then
        pip install uvicorn 
    fi
    deactivate
    cd ..
}

check_port_running() {
    if lsof -i :$PORT; then
        echo "A process is already using port $PORT."
        while true; do
            read -p "Do you want to stop this process and continue? (y/n) [default: y]: " stop_response
            stop_response=${stop_response:-y}
            if [[ "$stop_response" =~ ^[Yy]$ ]]; then
                sudo fuser -k $PORT/tcp
                echo -e "\033[0;32mProcess on port $PORT has been killed.\033[0m"
                break
            elif [[ "$stop_response" =~ ^[Nn]$ ]]; then
                echo -e "\033[0;31mThe process on port $PORT will not be stopped. Exiting setup.\033[0m"
                exit 1
            else
                echo -e "\033[0;31mInvalid input. Please enter 'y' or 'n'.\033[0m"
            fi
        done
    fi
}

check_startup() {
    if systemctl is-enabled --quiet perflect_dashboard.service; then
        echo "Perflect Dashboard is already set to start on boot."
        STARTUP_ADDED=true
        while true; do
            read -p "Do you want to remove it from startup? (y/n) [default: y]: " remove_response
            remove_response=${remove_response:-y}
            if [[ "$remove_response" =~ ^[Yy]$ ]]; then
                sudo systemctl disable perflect_dashboard.service
                sudo systemctl stop perflect_dashboard.service
                STARTUP_ADDED=false
                echo -e "\033[0;32mPerflect Dashboard has been removed from startup.\033[0m"
                break
            elif [[ "$remove_response" =~ ^[Nn]$ ]]; then
                break
            else
                echo -e "\033[0;31mInvalid input. Please enter 'y' or 'n'.\033[0m"
            fi
        done
    else
        echo "Perflect Dashboard is not set to start on boot."
        while true; do
            read -p "Do you want to add it to startup? (y/n) [default: y]: " add_response
            add_response=${add_response:-y}
            if [[ "$add_response" =~ ^[Yy]$ ]]; then
                echo -e "[Unit]
Description=Perflect Dashboard
After=network.target

[Service]
User=$USER
WorkingDirectory=$PWD/app
ExecStart=$PWD/app/myenv/bin/python -m uvicorn main:app --reload --host $IP --port $PORT
Restart=always

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/perflect_dashboard.service > /dev/null

                sudo systemctl daemon-reload
                sudo systemctl enable perflect_dashboard.service
                sudo systemctl start perflect_dashboard.service
                STARTUP_ADDED=true
                echo -e "\033[0;32mPerflect Dashboard has been set to start automatically on boot.\033[0m"
                break
            elif [[ "$add_response" =~ ^[Nn]$ ]]; then
                STARTUP_ADDED=false
                break
            else
                echo -e "\033[0;31mInvalid input. Please enter 'y' or 'n'.\033[0m"
            fi
        done
    fi
}

start_application() {
    cd "app"
    source myenv/bin/activate
    nohup myenv/bin/python -m uvicorn main:app --reload --host $IP --port $PORT > /dev/null 2>&1 &
    echo -e "\033[0;32mVisit the website at http://$IP:$PORT\033[0m"
    deactivate
    cd ..
}

main() {
    check_config
    if [ "$FLAG" = true ]; then
        echo "The dashboard is already ON. Do you want to terminate it?"
        while true; do
            read -p "Terminate the current dashboard? (y/n) [default: y]: " terminate_response
            terminate_response=${terminate_response:-y}
            if [[ "$terminate_response" =~ ^[Yy]$ ]]; then
                ./terminated.sh
                break
            elif [[ "$terminate_response" =~ ^[Nn]$ ]]; then
                echo -e "\033[0;31mExiting setup.\033[0m"
                exit 1
            else
                echo -e "\033[0;31mInvalid input. Please enter 'y' or 'n'.\033[0m"
            fi
        done
    fi

    if [ -n "$START_TIME" ]; then
        echo "Dashboard started at: $START_TIME"
    fi

    while true; do
        read -p "Enter the port (default: 9393): " user_port
        if [ -z "$user_port" ]; then
            user_port=9393
        fi
        if validate_port "$user_port"; then
            if check_port_availability "$user_port"; then
                PORT=$user_port
                break
            fi
        fi
    done

    while true; do
        read -p "Enter the IP (default: 127.0.0.1): " user_ip
        if [ -z "$user_ip" ]; then
            user_ip="127.0.0.1"
        fi
        if validate_ip "$user_ip"; then
            IP=$user_ip
            break
        fi
    done

    setup
    check_port_running
    check_startup
    start_application
    save_config
}

main
