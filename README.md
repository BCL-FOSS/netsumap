# netsumap 🔥🗺️
## Threat Management & Network Automation Platform ##

### EXPERIMENTAL 👨🏽‍💻 🔬 

<p align="center">
  <img width="300" height="300" src="https://github.com/BCL-FOSS/net-con.ai/blob/experimental/netsumapicon.png?raw=true">
</p>


### What is this?
Quart app using a neural network (NN) trained to classify IP packets as benign, outlier or malicious. Packet data is ingested via:
- pcap files converted to CSV, 
- JSON and 
- live capture from a specified interface (*currently in development). 

Prediction results are used to automate security breach responses within REST API enabled network infrastructure commonly utilized by SMBs. 

Training was conducted using traffic captured using the [Cisco Mercury](https://github.com/cisco/mercury) network metadata analysis tool from two sources:
- Honey pot hosted & managed by Baugh Consulting & Lab L.L.C.
- Simulated production corporate network with commonly utilized services & servers, and an "attacker" host targeting the resources with various attacks internally & externally. This allows for fine tuning of the data the model is trained on, increasing it's usability in various threat mitigation automation use cases.

As further research is conducted, the environments used for telemetry collection will become more complex to match the ever changing landscape of cybersecurity threats and improve the quality of the data used for training.

[Hugging Face Model Repo](https://huggingface.co/bclai) *NN model will be published soon

Current Integrations:
- Ubiquiti UniFi Network

Upcoming Integrations 👀:
- Live packet capture analysis
- Cisco Meraki
- Sonicwall
- HPE Aruba
- NETCONF/YANG configuration(s) generation based on pcap analysis results for wider integration with more complex systems. 

### What's Inside?

- 🐍 Python 
- 🧠 Machine Learning
- 📱 Mobile App for network status monitoring

### How would I use this?
There are two ways you can use this product, either as a traffic analysis tool for your network, or as a platform to start automating network management functions with ML. 

### Getting Started

#### Recommended Environment
- Ubuntu 22.04 LTS
- 1/12 GPU Minimum
- 4 GB GPU Mem. Minimum

#### Backend Environment Setup

1. Install CUDA Driver
2. [Install CUDA Toolkit](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=runfile_local)

3. Install Nvidia CUDA Compiler
```python
    pip install nvidia-pyindex
    pip install nvidia-cuda-nvcc
```
4. Install Docker
```bash
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
``` 
5. Install Redis DB
```bash
    sudo apt-get install lsb-release curl gpg
    curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
    sudo chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
    sudo apt-get update
    sudo apt-get install redis

```
5. Build custom docker image 
```bash
    cd /Docker
    sudo docker build -t netsumap-tensorflow .
```
6. Run custom Docker Image
```bash
    sudo docker run --gpus all --name netsumap -d -it -v $(pwd):$(pwd) -w $(pwd) docker.io/library/netsumap-tensorflow
```
7. Access shell for netsumap container
```bash
    sudo docker exec -it netsumap bash
```
8. Start App
```bash
    hypercorn app:app --bind '0.0.0.0:25000'
``` 

#### Websocket Environment Setup

```bash
    git clone 
    cd netsumap/socket/
    apt install python3.12-venv
    python3 -m venv .venv 
    . .venv/bin/activate
    pip install poetry 
    poetry install
    cd socket/src/socket/
    hypercorn app:app --bind '0.0.0.0:30000'
```









