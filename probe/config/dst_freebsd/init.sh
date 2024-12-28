#!/bin/bash

# Function to check if it's pfSense
is_pfsense() {
    if [ -f "/etc/pfsense-release" ]; then
        return 0  # It is pfSense
    else
        return 1  # It is not pfSense
    fi
}

# Function to check if it's OPNsense
is_opnsense() {
    if [ -f "/usr/local/etc/os-release" ] && grep -q "OPNsense" /usr/local/etc/os-release; then
        return 0  # It is OPNsense
    else
        return 1  # It is not OPNsense
    fi
}

# Open port function for pfSense
open_pfsense_port() {
    RULE="pass in on em0 proto tcp from any to any port 5000"
    echo "$RULE" >> /etc/pf.conf
    pfctl -f /etc/pf.conf
    pfctl -e
    echo "Port 5000 opened on pfSense."
}

# Open port function for OPNsense
open_opnsense_port() {
    RULE="pass in on em0 proto tcp from any to any port 5000"
    echo "$RULE" >> /etc/pf.conf
    pfctl -f /etc/pf.conf
    pfctl -e
    echo "Port 5000 opened on OPNsense."
}

# Open port function for regular FreeBSD
open_freebsd_port() {
    # Open port 5000 in a generic FreeBSD system (non pfSense/OPNsense)
    RULE="pass in proto tcp from any to any port 5000"
    echo "$RULE" >> /etc/pf.conf

    # Reload pf firewall configuration
    pfctl -f /etc/pf.conf
    pfctl -e
    echo "Port 5000 opened on regular FreeBSD system."
}

install_probe_dependencies(){
    # Update the FreeBSD package repository
    echo "Updating FreeBSD package repository..."
    pkg update

    # Ensure Python and pip are installed
    echo "Checking for Python installation..."
    if ! command -v python3 > /dev/null 2>&1; then
        echo "Python3 is not installed. Installing Python3..."
        pkg install -y python3
    fi

    if ! command -v pip > /dev/null 2>&1; then
        echo "pip is not installed. Installing pip..."
        pkg install -y py39-pip  # Adjust version as needed
    fi

    # Install iperf3
    if ! command -v iperf3 > /dev/null 2>&1; then
        echo "Installing iperf3..."
        pkg install -y iperf3
    else
        echo "iperf3 is already installed."
    fi

    # Install p0f
    if ! command -v p0f > /dev/null 2>&1; then
        echo "Installing p0f..."
        pkg install -y p0f
    else
        echo "p0f is already installed."
    fi

    # Install tshark
    if ! command -v tshark > /dev/null 2>&1; then
        echo "Installing tshark..."
        pkg install -y tshark
    else
        echo "tshark is already installed."
    fi

    echo "Installation of tools completed."
}

# Main logic

install_probe_dependencies

if is_pfsense; then
    echo "System is running pfSense."
    open_pfsense_port
elif is_opnsense; then
    echo "System is running OPNsense."
    open_opnsense_port
else
    echo "Neither pfSense nor OPNsense detected. Proceeding with normal FreeBSD firewall configuration."
    open_freebsd_port
fi

# Print current firewall rules
pfctl -sr