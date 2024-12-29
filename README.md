# netsumap

## Open Source Event Management & Monitoring for Unix & Linux Infrastructure
#### EXPERIMENTAL & CURRENTLY UNDER DEVELOPMENT 🔬 
<p align="center">
  <img width="300" height="300" src="https://github.com/BCL-FOSS/net-con.ai/blob/experimental/netsumapicon.png?raw=true">
</p>

### What is this?
A simple, easy to deploy monitoring & event management system for critical FreeBSD & Linux servers.

### Features
- Service + Network Outage Alerts
- Infrastructure Monitoring for FreeBSD, RHEL & Debian systems
- Network Visualizer + Mapper
- Integrated Neural Network performing:
    + 👨🏽‍💻 Packet metadata analysis 
    + 💥 Attack pattern identification 

NN training data captured from: 
- Honey pot(s) hosted & managed by Baugh Consulting & Lab L.L.C.
- Simulated production corporate network with commonly utilized services & servers, and an "attacker" host targeting the resources with various attacks internally & externally.

[Hugging Face Model Repo](https://huggingface.co/bclai) *NN to be published soon

## Getting Started
#### Core Configuration

##### Recommended Minimum Environment
- Ubuntu 22.04 LTS
- 1/12 GPU 
- 4 GB GPU Memory 
- 8 GB RAM

1. Install CUDA Driver
2. [Install CUDA Toolkit](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=runfile_local)
3. Update core-node/Caddyfile with new url
```bash
    change.url.com {
        ...
    }
```
4. Run startup script (starts netsumap core after initialization)
```bash
    sudo ./netsumap_init.sh
```
5. Visit core dashboard @ [https://url-set-in-Caddyfile.com/] to get started.

To restart netsumap 
```bash
    sudo ./netsumap_restart.sh
```










