# netsumap
## Threat Management & Network Automation ##
### EXPERIMENTAL 🔬 
<p align="center">
  <img width="300" height="300" src="https://github.com/BCL-FOSS/net-con.ai/blob/experimental/netsumapicon.png?raw=true">
</p>

### What is this?
Quart app leveraging a neural network (NN) to identify patterns of an attack in progress within a network. Predicitons are used to automate security breach responses within REST API enabled network infrastructure.

Data captured from: 
- Honey pot hosted & managed by Baugh Consulting & Lab L.L.C.
- Simulated production corporate network with commonly utilized services & servers, and an "attacker" host targeting the resources with various attacks internally & externally.

[Hugging Face Model Repo](https://huggingface.co/bclai) *NN model will be published soon

### Use Cases
- 👨🏽‍💻 traffic metadata analysis
- 💥 attack pattern identification 
- 🤖 network automation
- 📱 self hosted netadmin mobile app (*currently in development)

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

### Recommended Minimum Environment
- Ubuntu 22.04 LTS
- 1/12 GPU 
- 4 GB GPU Memory 
- 8 GB RAM

### Core Configuration
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
6. Install Redis DB (optional depending on if the mobile app is being utilized)
```bash
    sudo apt-get install lsb-release curl gpg
    curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
    sudo chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
    sudo apt-get update
    sudo apt-get install redis

```












