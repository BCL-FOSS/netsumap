#!/bin/bash

open_rhel_port() {
    echo "Opening port 5000 on RHEL system..."
    sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT

    if command -v firewall-cmd > /dev/null 2>&1; then
        sudo firewall-cmd --permanent --add-port=5000/tcp
        sudo firewall-cmd --reload
    elif command -v iptables-save > /dev/null 2>&1 && command -v iptables-restore > /dev/null 2>&1; then
        sudo iptables-save > /etc/sysconfig/iptables
    else
        echo "Warning: iptables persistence is not configured. Rules will not persist after reboot."
    fi

    echo "Port 5000 opened on RHEL system."
}

install_probe_dependencies() {
    echo "Updating RHEL package repository..."
    sudo yum update -y || sudo dnf update -y

    echo "Checking for Python installation..."
    if ! command -v python3 > /dev/null 2>&1; then
        echo "Python3 is not installed. Installing Python3..."
        sudo yum install -y python3
    fi

    if ! command -v pip3 > /dev/null 2>&1; then
        echo "pip3 is not installed. Installing pip3..."
        sudo yum install -y python3-pip
    fi

    echo "Checking for python3-venv installation..."
    if ! rpm -q python3-venv > /dev/null 2>&1; then
        echo "python3-venv is not installed. Installing python3-venv..."
        sudo yum install -y python3-venv
    else
        echo "python3-venv is already installed."
    fi

    if ! command -v iperf3 > /dev/null 2>&1; then
        echo "Installing iperf3..."
        sudo yum install -y iperf3
    else
        echo "iperf3 is already installed."
    fi

    if ! command -v p0f > /dev/null 2>&1; then
        echo "Installing p0f..."
        sudo yum install -y p0f
    else
        echo "p0f is already installed."
    fi

    if ! command -v tshark > /dev/null 2>&1; then
        echo "Installing tshark..."
        sudo yum install -y wireshark
    else
        echo "tshark is already installed."
    fi

    echo "Installation of tools completed."
}

# Main
install_probe_dependencies
open_rhel_port
