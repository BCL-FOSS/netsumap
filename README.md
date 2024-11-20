# netsumap
## Threat Management & Network Automation ##
### EXPERIMENTAL 🔬 
<p align="center">
  <img width="300" height="300" src="https://github.com/BCL-FOSS/net-con.ai/blob/experimental/netsumapicon.png?raw=true">
</p>

### What is this?
This initially started as a Quart app meant to do the following:
- 👨🏽‍💻 traffic metadata analysis
- 💥 attack pattern identification 
- 🤖 network automation

It's currently turning into an infrastructure monitoring & management tool, with network metadata analysis, automation & data visualizations built in. 

The "core" controls the "probes", with probes being either:
- a self contained server in capture mode
- existing infrastructure hosting a critical service (in this case the core would be monitoring the service & host).

Model training data captured from: 
- Honey pot(s) hosted & managed by Baugh Consulting & Lab L.L.C.
- Simulated production corporate network with commonly utilized services & servers, and an "attacker" host targeting the resources with various attacks internally & externally.

[Hugging Face Model Repo](https://huggingface.co/bclai) *NN model will be published soon

#### Current Integrations
- Ubiquiti UniFi Network
- JSON, CSV network metadata analysis
- Live packet capture + analysis
- Uptime monitoring 

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
3. Open port necessary ports
```bash
    sudo ufw allow 80
    sudo ufw allow 443
```
4. Install CUDA Compiler  
```python
    pip install nvidia-pyindex 
    pip install nvidia-cuda-nvcc
```
5. Run startup script (starts netsumap after initialization)
```bash
    sudo ./netsumap_init.sh
```
6. Visit netsumap core @ [https://your-core-node-domain.com/] to get started.

To restart netsumap 
```bash
    sudo ./netsumap_restart.sh
```

### Network Probe Configuration
1. Initialize the probe, will create a cronjob which runs packet capture every 5 minutes (can be adjusted)
```bash
    sudo ./inf_init.sh

    # probe parameters require the core-node URL & the # of packets to capture for analysis. Example:

    [https://your-core-node-domain.com/] 50
```

Run pcap session for instant analysis (same parameters as init script)
```bash
    sudo ./inf_run.sh
```









