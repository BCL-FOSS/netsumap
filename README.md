# netsumap
## Threat Management & Network Automation ##
### EXPERIMENTAL 🔬 
<p align="center">
  <img width="300" height="300" src="https://github.com/BCL-FOSS/net-con.ai/blob/experimental/netsumapicon.png?raw=true">
</p>

### What is this?
Quart app using a neural network (NN) trained to classify network traffic metadata as benign, outlier or malicious. Packet data is ingested via pcap files converted to CSV, JSON and live capture from specified interface (*currently in development). Prediction results are used to automate security breach responses within REST API enabled network infrastructure commonly utilized by SMBs. 

Training was conducted using traffic captured using [Cisco Mercury](https://github.com/cisco/mercury)from two sources:
- Honey pot hosted & managed by Baugh Consulting & Lab L.L.C.
- Simulated production corporate network with commonly utilized services & servers, and an "attacker" host targeting the resources with various attacks internally & externally.

[Hugging Face Model Repo](https://huggingface.co/bclai) *NN model will be published soon

### How would I use this?
netsumap can be utilized in the following usecases:
- 👨🏽‍💻 traffic metadata analysis
- 💥 attack pattern identification 
- 🤖 network automation
- 📱 self hosted mobile network status monitoring & management (*currently in development)

#### Current Integrations
- Ubiquiti UniFi Network

#### Upcoming Integrations 👀
- Live packet capture analysis
- Cisco Meraki
- Sonicwall
- HPE Aruba
- NETCONF/YANG configuration(s) generation

## Getting Started

### Recommended Environment
- Ubuntu 22.04 LTS
- 1/12 GPU Minimum
- 4 GB GPU Memory Minimum
- 8 GB RAM Minimum

### Core Configuration
1. Install CUDA Driver
2. [Install CUDA Toolkit](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=runfile_local)

3. Install Nvidia CUDA Compiler
```python
    pip install nvidia-pyindex
    pip install nvidia-cuda-nvcc
```
4. Open port 25000
```bash
    sudo ufw allow 25000
```
5. Run startup script 
```bash
    sudo ./netsumap_init.sh
```
5. Install Redis DB (optional depending on if the mobile app is being utilized)
```bash
    sudo apt-get install lsb-release curl gpg
    curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
    sudo chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
    sudo apt-get update
    sudo apt-get install redis

```












