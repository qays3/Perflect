#!/bin/bash

DIR="./app"
CONFIG_FILE="$DIR/setup.ini"

load_config() {
    if [ -f "$CONFIG_FILE" ]; then
        while IFS='=' read -r key value; do
            if [[ ! -z "$key" && ! -z "$value" ]]; then
                 
                value=$(echo "$value" | sed -e 's/^"//' -e 's/"$//')
                export "$key"="$value"
            fi
        done < "$CONFIG_FILE"
    else
        echo -e "\033[0;31mNo setup.ini file found. Exiting.\033[0m"
        exit 1
    fi
}

convert_seconds_to_readable() {
    local seconds=$1
    local days=$((seconds / 86400))
    local hours=$((seconds % 86400 / 3600))
    local minutes=$((seconds % 3600 / 60))
    local secs=$((seconds % 60))
    echo "${days}d ${hours}h ${minutes}m ${secs}s"
}

calculate_uptime() {
    TERMINATED_TIME=$(date '+%Y-%m-%d %H:%M:%S')
    if [ -n "$START_TIME" ]; then
        START_TIMESTAMP=$(date -d "$START_TIME" +%s)
        TERMINATED_TIMESTAMP=$(date -d "$TERMINATED_TIME" +%s)
        UPTIME=$((TERMINATED_TIMESTAMP - START_TIMESTAMP))
        UPTIME_READABLE=$(convert_seconds_to_readable $UPTIME)
        {
            echo "TOTAL_UPTIME=\"$UPTIME_READABLE\""
            echo "TERMINATED_TIME=\"$TERMINATED_TIME\""
        } >> "$CONFIG_FILE"
        echo -e "\033[0;32mDashboard was running for $UPTIME_READABLE.\033[0m"
    else
        echo -e "\033[0;31mNo start time found in setup.ini.\033[0m"
    fi
}

turn_off_dashboard() {
    echo "Turning off the Dashboard..."
    sudo systemctl stop perflect_dashboard.service
    echo -e "\033[0;32mDashboard has been turned off.\033[0m"
}

remove_from_startup() {
    if [ "$STARTUP_ADDED" = true ]; then
        echo "Removing Dashboard from startup..."
        sudo systemctl disable perflect_dashboard.service
        sudo systemctl stop perflect_dashboard.service
        echo -e "\033[0;32mDashboard has been removed from startup.\033[0m"
    else
        echo -e "\033[0;33mDashboard is not set to start on boot. Skipping.\033[0m"
    fi
}

close_port() {
    echo "Closing port $PORT..."
    PID=$(sudo lsof -t -i :$PORT)
    if [ -n "$PID" ]; then
        sudo kill -9 $PID
        echo -e "\033[0;32mPort $PORT has been closed.\033[0m"
    else
        echo -e "\033[0;31mNo process found using port $PORT.\033[0m"
    fi
}

main() {
    load_config
    if [ -n "$START_TIME" ]; then
        echo "Dashboard started at: $START_TIME"
    fi

    while true; do
        read -p "Do you want to turn off the Dashboard? (y/n) [default: y]: " turn_off_response
        turn_off_response=${turn_off_response:-y}
        if [[ "$turn_off_response" =~ ^[Yy]$ ]]; then
            turn_off_dashboard
            break
        elif [[ "$turn_off_response" =~ ^[Nn]$ ]]; then
            echo -e "\033[0;33mDashboard will not be turned off.\033[0m"
            exit 0
        else
            echo -e "\033[0;31mInvalid input. Please enter 'y' or 'n'.\033[0m"
        fi
    done

    if [ "$STARTUP_ADDED" = true ]; then
        while true; do
            read -p "Do you want to remove the Dashboard from startup? (y/n) [default: y]: " remove_startup_response
            remove_startup_response=${remove_startup_response:-y}
            if [[ "$remove_startup_response" =~ ^[Yy]$ ]]; then
                remove_from_startup
                break
            elif [[ "$remove_startup_response" =~ ^[Nn]$ ]]; then
                break
            else
                echo -e "\033[0;31mInvalid input. Please enter 'y' or 'n'.\033[0m"
            fi
        done
    fi

    while true; do
        read -p "Do you want to close the port? (y/n) [default: y]: " close_port_response
        close_port_response=${close_port_response:-y}
        if [[ "$close_port_response" =~ ^[Yy]$ ]]; then
            close_port
            break
        elif [[ "$close_port_response" =~ ^[Nn]$ ]]; then
            break
        else
            echo -e "\033[0;31mInvalid input. Please enter 'y' or 'n'.\033[0m"
        fi
    done

    calculate_uptime
    sed -i '/^FLAG=true$/,/^$/s/^FLAG=true$/FLAG=false/' "$CONFIG_FILE"
    echo -e "\033[0;32mTermination process completed.\033[0m"
}

main