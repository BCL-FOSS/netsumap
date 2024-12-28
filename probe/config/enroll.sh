#!/bin/bash

create_checkin_cronjob() {
    script="$WRKDIR/ping.py"

    echo $script
    if [ ! -f $script ]; then
        echo "Error: File does not exist"
        exit 1
    fi

    CRON_JOB="*/5 * * * * python3 $script"

    (sudo crontab -l | grep -F "$CRON_JOB") > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        echo "Cron job already exists. No changes made."
    else
        (sudo crontab -l; echo "$CRON_JOB") | sudo crontab -

        echo "Cron job added to run the script every 5 minutes with parameters: $COREURL"
    fi
}

get_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    elif [ -f /etc/redhat-release ]; then
        echo "rhel"
    elif [ -f /etc/debian_version ]; then
        echo "debian"
    elif [ -f /usr/share/man/man1/freebsd-update.1.gz ]; then
        echo "freebsd"
    else
        echo "unknown"
    fi
}

setup_debian() {
    echo "Detected Debian-based system. Running probe configuration..."
    sudo apt update && sudo apt upgrade -y

    script_dir="$WRKDIR/dst_debian"

    script="$script_dir/init.sh"

    if [ ! -f $script ]; then
        echo "Error: File does not exist"
        exit 1
    fi

    sudo chmod +x $script

    sudo ./$script

    create_venv

    python3 cfg.py --url $COREURL --enroll

    source "$VENV_DIR/bin/deactivate"
}

setup_rhel() {
    echo "Detected RHEL-based system. Running probe configuration..."
    sudo dnf update && sudo dnf upgrade -y || sudo yum update -y && sudo yum upgrade -y

    script_dir="$WRKDIR/dst_rhel"

    script="$script_dir/init.sh"

    if [ ! -f $script ]; then
        echo "Error: File does not exist"
        exit 1
    fi

    sudo chmod +x $script

    sudo ./$script

    create_venv

    python3 cfg.py --url $COREURL --enroll

    source "$VENV_DIR/bin/deactivate"
}

setup_freebsd() {
    echo "Detected FreeBSD-based system. Running probe configuration..."
    sudo pkg update -y && sudo pkg upgrade -y

    script_dir="$WRKDIR/dst_freebsd"

    script="$script_dir/init.sh"

    if [ ! -f $script ]; then
        echo "Error: File does not exist"
        exit 1
    fi

    sudo chmod +x $script

    sudo ./$script

    create_venv

    python3 cfg.py --url $COREURL --enroll

    source "$VENV_DIR/bin/deactivate"
}

create_venv() {
    VENV_DIR="$WRKDIR"
    if [[ ! -d "$VENV_DIR" ]]; then
        echo "Creating a virtual environment in '$VENV_DIR'..."
        python3 -m venv "$VENV_DIR"

        echo "Activating the virtual environment..."
        source "$VENV_DIR/bin/activate"

        echo "Upgrading pip in the virtual environment..."
        pip install --upgrade pip

        echo "Installing packages from requirements.txt..."
        pip install --no-cache-dir -r requirements.txt --upgrade

        echo "Setup complete. To activate the virtual environment, run:"
        echo "source $VENV_DIR/bin/activate"
    else
        echo "Virtual environment already exists in '$VENV_DIR'."

        echo "Activating the virtual environment..."
        source "$VENV_DIR/bin/activate"

        echo "Upgrading pip in the virtual environment..."
        pip install --upgrade pip

        echo "Installing packages from requirements.txt..."
        pip install --no-cache-dir -r requirements.txt --upgrade
    fi
}

# Main
WRKDIR="$(cd "$(dirname "$0")"; pwd)"

echo $WRKDIR

echo "Enter core-node url without trailing '/':"
echo "https://your-netsumap-core-url"

read -p "Core URL: " SCRIPT_PARAMS

COREURL="$SCRIPT_PARAMS"

echo $COREURL

DISTRIBUTION=$(get_distro)

case "$DISTRIBUTION" in
    debian|ubuntu)
        echo "Detected Debian-based system. Running probe configuration..."
        setup_debian
        ;;
    rhel|centos|fedora|rocky|almalinux)
        echo "Detected RHEL-based system. Running probe configuration..."
        setup_rhel
        ;;
    freebsd)
        echo "Detected FreeBSD system. Running probe configuration..."
        setup_freebsd
        ;;
    *)
        echo "Unknown or unsupported distribution. Exiting."
        exit 1
        ;;
esac

create_checkin_cronjob

