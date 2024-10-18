# net-con.ai
## Threat Management & Network Automation Platform ##

### EXPERIMENTAL ###

### What is this?
Quart app using an internally developed Keras model trained to classify IP packets as benign, outlier or malicious. Packet data is ingested via pcap files converted to CSV files and the /threat_analysis endpoint.

Current Integrations:
- Ubiquiti UniFi

Upcoming Integrations 👀:
- Cisco Meraki
- Sonicwall
- HPE Aruba

### What's Inside?

- 🐍 Python 
- 🧠 AI
- 📱 Mobile App for network status monitoring

### Getting Started

#### Recommended Environment
- Ubuntu 22.04 LTS
- 1/12 GPU Minimum
- 4 GB GPU Mem. Minimum

#### Backend Environment Setup

1. Install CUDA Driver (if necessary)
2. [Install CUDA Toolkit](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=runfile_local)
3. ```python
    pip3 install tensorflow[and-cuda]
    ``` 
4. ```bash
    sudo apt-get install pandoc
    sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-plain-generic
    sudo apt-get install libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 libatspi2.0-0 libxcomposite1 libxdamage1 libxrandr2 libpango-1.0-0 libasound2

    ```
5. ```python
    pip3 install quart pandas numpy matplotlib seaborn scikit-learn fpdf2 jupyter ipykernel nbconvert pyppeteer nbconvert[webpdf]
    ``` 
6. ```bash
    playwright install chromium
    sudo playwright install-deps
    ```
7. ```bash
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






