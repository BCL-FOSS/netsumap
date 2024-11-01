# netsumap 🔥🗺️
## Threat Management & Network Automation Platform ##

### EXPERIMENTAL 👨🏽‍💻 🔬 

<p align="center">
  <img width="300" height="300" src="https://github.com/BCL-FOSS/net-con.ai/blob/experimental/netsumapicon.png?raw=true">
</p>


### What is this?
Quart app using a neural network (NN) trained to classify IP packets as benign, outlier or malicious. Packet data is ingested via pcap files converted to CSV, JSON and live capture from a specified interface (*currently in development). The prediction results are used to automate security breach responses within REST API enabled network infrastructure commonly utilized by SMBs. 

The NN was initially trained on data captured with the [Cisco Mercury](https://github.com/cisco/mercury) network metadata analysis tool. Traffic was generated in a simulated environment with a vulnerable VMs hosting several applications, and a Kali Linux VM simulating various attacks. As further research is conducted, the simulation environment will become more complex to match the ever changing landscape of cybersecurity threats and improve the quality of the data used for training.

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

1. Install CUDA Driver (if necessary)
2. [Install CUDA Toolkit](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=runfile_local)
3. Install Tensorflow GPU version
    ```python
    pip3 install tensorflow[and-cuda]
    ``` 
4. Install Redis DB (only necessary if using the mobile app and Ubiquiti UniFi Network integration)
    ```bash
    sudo apt-get install lsb-release curl gpg
    curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
    sudo chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
    sudo apt-get update
    sudo apt-get install redis

    ```
5.  Install necessary libraries 
    ```python
    pip3 install quart pandas numpy matplotlib seaborn scikit-learn ipykernel asyncio-redis redis Werkzeug flask_cors nest_asyncio
    ``` 
6. Install optional Python libraries (for data visualization)
    ```python
    pip3 install fpdf2 jupyter ipykernel nbconvert pyppeteer nbconvert[webpdf] 
    ``` 
7. Install Optional dependencies (for data visualization)
    ```bash
    sudo apt-get install pandoc
    sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-plain-generic
    sudo apt-get install libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 libatspi2.0-0 libxcomposite1 libxdamage1 libxrandr2 libpango-1.0-0 libasound2
    playwright install chromium
    sudo playwright install-deps

    ```
8. Start App
    ```bash
    cd net-con.ai/backend/src/backend/

    hypercorn app:app --bind '0.0.0.0:25000'
    ``` 

#### Websocket Environment Setup
* git clone 
* cd net-con.ai/socket/
* apt install python3.12-venv
* python3 -m venv .venv 
* . .venv/bin/activate
* pip install poetry 
* poetry install
* cd socket/src/socket/
* hypercorn app:app --bind '0.0.0.0:30000'






