#!/bin/bash

# Open port function for Debian-based systems
open_debian_port() {
    # Open port 5000 in a generic Debian system using iptables
    echo "Opening port 5000 on Debian system..."
    iptables -A INPUT -p tcp --dport 5000 -j ACCEPT

    # Save iptables rules to ensure persistence across reboots
    if command -v netfilter-persistent > /dev/null 2>&1; then
        netfilter-persistent save
    elif command -v iptables-save > /dev/null 2>&1 && command -v iptables-restore > /dev/null 2>&1; then
        iptables-save > /etc/iptables/rules.v4
    else
        echo "Warning: iptables persistence is not configured. Rules will not persist after reboot."
    fi

    echo "Port 5000 opened on Debian system."
}

install_probe_dependencies() {
    # Update the Debian package repository
    echo "Updating Debian package repository..."
    apt update -y

    # Ensure Python, pip, and venv are installed
    echo "Checking for Python installation..."
    if ! command -v python3 > /dev/null 2>&1; then
        echo "Python3 is not installed. Installing Python3..."
        apt install -y python3
    fi

    if ! command -v pip3 > /dev/null 2>&1; then
        echo "pip3 is not installed. Installing pip3..."
        apt install -y python3-pip
    fi

    echo "Checking for python3-venv installation..."
    if ! dpkg -l | grep -qw python3-venv; then
        echo "python3-venv is not installed. Installing python3-venv..."
        apt install -y python3-venv
    else
        echo "python3-venv is already installed."
    fi

    # Install iperf3
    if ! command -v iperf3 > /dev/null 2>&1; then
        echo "Installing iperf3..."
        apt install -y iperf3
    else
        echo "iperf3 is already installed."
    fi

    # Install p0f
    if ! command -v p0f > /dev/null 2>&1; then
        echo "Installing p0f..."
        apt install -y p0f
    else
        echo "p0f is already installed."
    fi

    # Install tshark
    if ! command -v tshark > /dev/null 2>&1; then
        echo "Installing tshark..."
        apt install -y tshark
    else
        echo "tshark is already installed."
    fi

    echo "Installation of tools completed."
}


# Main logic
install_probe_dependencies
open_debian_port



