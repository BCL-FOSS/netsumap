# netsumap
## Threat Management & Network Automation ##
### EXPERIMENTAL 🔬 
<p align="center">
  <img width="300" height="300" src="https://github.com/BCL-FOSS/net-con.ai/blob/experimental/netsumapicon.png?raw=true">
</p>

### What is this?
Quart app leveraging a neural network (NN) to identify patterns of an attack in LAN, WAN & cloud environments. Predicitons are used to automate security breach responses within REST API enabled network infrastructure.

A single core-node manages deployed probes, which periodically send relevant traffic metadata gathered from specified interfaces back to the core for preprocessing and inference. 

Model training data captured from: 
- Honey pot(s) hosted & managed by Baugh Consulting & Lab L.L.C.
- Simulated production corporate network with commonly utilized services & servers, and an "attacker" host targeting the resources with various attacks internally & externally.

[Hugging Face Model Repo](https://huggingface.co/bclai) *NN model will be published soon

### Use Cases
- 👨🏽‍💻 traffic metadata analysis
- 💥 attack pattern identification 
- 🤖 network automation

#### Current Integrations
- Ubiquiti UniFi Network
- JSON, CSV network metadata analysis
- Live packet capture + analysis

#### Upcoming Integrations 👀
- Cisco Meraki
- Sonicwall
- HPE Aruba
- NETCONF/YANG configuration(s) generation

## Getting Started

### Core Configuration

#### Recommended Minimum Environment
- Ubuntu 22.04 LTS
- 1/12 GPU 
- 4 GB GPU Memory 
- 8 GB RAM

1. Install CUDA Driver
2. [Install CUDA Toolkit](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=runfile_local)
3. Open port 25000
```bash
    sudo ufw allow 25000
```
4. Install CUDA Compiler  
```python
    pip install nvidia-pyindex 
    pip install nvidia-cuda-nvcc
```
5. Run startup script 
```bash
    sudo ./netsumap_init.sh
```
6. Visit the dashboard at [https://core-server-ip:25000/] to get started.

To restart netsumap 
```bash
    sudo ./netsumap_restart.sh
```

### Network Probe Configuration
1. Setup environment
```bash
    sudo apt update -y
    sudo apt upgrade -y

    sudo apt install -y python3.12-venv
    python3.12 -m venv venv
    . venv/bin/activate
    pip install scapy requests
```
2. Initialize the probe, will create a cronjob which runs packet capture every 5 minutes (can be adjusted)
```bash
    sudo ./inf_init.sh

    # probe parameters require the core-node URL & the # of packets to capture for analysis. Example:

    http://0.0.0.0:25000 50 ws://1.1.1.1:30000/
```

Run pcap session for instant analysis
```bash
    sudo ./inf_run.sh
```

### Websocket Configuration
1. Open Port 30000
```bash
    sudo ufw allow 30000
``` 
2. Run setup script
```bash
    sudo ./ws_init.sh
``` 
Restart websocket
```bash
    sudo ./ws_restart.sh
```












