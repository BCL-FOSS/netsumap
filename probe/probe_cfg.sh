#!/bin/sh

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

create_checkin_cronjob() {
    if sudo crontab -l | grep -F "$CRON_JOB" > /dev/null 2>&1; then
        echo "Cron job already exists. No changes made."
    else
        (sudo crontab -l 2>/dev/null; echo "$CRON_JOB") | sudo crontab -
        echo "Cron job added to run the script every 5 minutes."
    fi
}

remove_checkin_cronjob() {
    if sudo crontab -l | grep -F "$CRON_JOB" > /dev/null 2>&1; then
        sudo crontab -l | grep -v "$CRON_JOB" | sudo crontab -
        echo "Cron job containing '$CRON_JOB' has been removed successfully."
    else
        echo "No cron job containing '$CRON_JOB' found. No changes made."
    fi
}

create_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        echo "Creating a virtual environment in '$VENV_DIR'..."
        python3 -m venv "$VENV_DIR"

        echo "Activating the virtual environment..."
        . "$VENV_DIR/bin/activate"

        echo "Upgrading pip in the virtual environment..."
        pip install --upgrade pip

        echo "Installing packages from requirements.txt..."
        pip install --no-cache-dir -r requirements.txt --upgrade

        echo "Setup complete. To activate the virtual environment, run:"
        echo "source $VENV_DIR/bin/activate"
    else
        echo "Virtual environment already exists in '$VENV_DIR'."

        echo "Activating the virtual environment..."
        . "$VENV_DIR/bin/activate"

        echo "Upgrading pip in the virtual environment..."
        pip install --upgrade pip

        echo "Installing packages from requirements.txt..."
        pip install --no-cache-dir -r requirements.txt --upgrade
    fi
}

config_freebsd() {
    init_script="$script_dir/dst_freebsd/init.sh"

    if [ "$1" = "--enroll" ]; then
        sudo pkg update -y && sudo pkg upgrade -y

        echo "Enter core-node URL without trailing '/':"
        echo "https://your-netsumap-core-url"
        read -p "Core URL: " COREURL

        echo "$COREURL"

        sudo chmod +x "$init_script"

        . "$init_script"

        create_venv

        python3 "$cfg_script" --url "$COREURL" "$1"

        . "$VENV_DIR/bin/deactivate"

        create_checkin_cronjob

    elif [ "$1" = "--unenroll" ]; then
        remove_checkin_cronjob

        . "$VENV_DIR/bin/activate"

        python3 "$cfg_script" "$2"

        . "$VENV_DIR/bin/deactivate"
    else
        echo "Usage: [--enroll | --unenroll]"
        exit 1
    fi
}

config_debian() {
    init_script="$script_dir/dst_debian/init.sh"

    if [ "$1" = "--enroll" ]; then
        sudo apt update && sudo apt upgrade -y

        echo "Enter core-node URL without trailing '/':"
        echo "https://your-netsumap-core-url"
        read -p "Core URL: " COREURL

        echo "$COREURL"
        sudo chmod +x "$init_script"
        . "$init_script"

        create_venv
        python3 "$cfg_script" --url "$COREURL" "$1"
        . "$VENV_DIR/bin/deactivate"

        create_checkin_cronjob
    elif [ "$1" = "--unenroll" ]; then
        . "$VENV_DIR/bin/activate"
        python3 "$cfg_script" "$1"
        . "$VENV_DIR/bin/deactivate"
        remove_checkin_cronjob
    else
        echo "Usage: [--enroll | --unenroll]"
        exit 1
    fi
}

config_rhel() {
    init_script="$script_dir/dst_rhel/init.sh"
    
    if [ "$1" = "--enroll" ]; then
        sudo dnf update -y || sudo yum update -y
        sudo dnf upgrade -y || sudo yum upgrade -y

        echo "Enter core-node URL without trailing '/':"
        echo "https://your-netsumap-core-url"
        read -p "Core URL: " COREURL

        echo "$COREURL"
        sudo chmod +x "$init_script"
        . "$init_script"

        create_venv
        python3 "$cfg_script" --url "$COREURL" "$1"
        . "$VENV_DIR/bin/deactivate"

        create_checkin_cronjob
    elif [ "$1" = "--unenroll" ]; then
        remove_checkin_cronjob

        . "$VENV_DIR/bin/activate"
        python3 "$cfg_script" "$1"
        . "$VENV_DIR/bin/deactivate"
    else
        echo "Usage: [--enroll | --unenroll]"
        exit 1
    fi
}

probecfg() {
    script_dir="$WRKDIR/config"
    cfg_script="$script_dir/cfg.py"
    checkin_script="$script_dir/ping.py"
    CRON_JOB="*/5 * * * * python3 $checkin_script"
    VENV_DIR="$WRKDIR/venv"

    DISTRIBUTION=$(get_distro)

    case "$DISTRIBUTION" in
        debian|ubuntu)
            echo "Detected Debian-based system. Running probe configuration..."
            config_debian "$1"
            ;;
        rhel|centos|fedora|rocky|almalinux)
            echo "Detected RHEL-based system. Running probe configuration..."
            config_rhel "$1"
            ;;
        freebsd)
            echo "Detected FreeBSD system. Running probe configuration..."
            config_freebsd "$1"
            ;;
        *)
            echo "Unknown or unsupported distribution. Exiting."
            exit 1
            ;;
    esac
}

# Main
WRKDIR="$(cd "$(dirname "$0")" && pwd)"
echo "$WRKDIR"

if [ "$1" = "--enroll" ]; then
    probecfg "$1"
elif [ "$1" = "--unenroll" ]; then
    probecfg "$1"
else
    echo "Usage: $0 [--enroll | --unenroll]"
    exit 1
fi
