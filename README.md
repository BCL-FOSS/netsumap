# NetiFi Dash #

## Self-hosted NOC Dashboard, DPI Threat Analysis & Admin Tool for Ubiquiti UniFi ##
### EXPERIMENTAL, WILL GO INTO PRODUCTION SOON ###

* [UbiquiPy Repo](https://github.com/BCL-FOSS/UbiquiPy-UniFi-Automation)
* [Learn more about UbiquiPy here](https://www.baughcl.com/ubiquipy.html) 
* Quart for asynchronous usage
* Caddy reverse proxy(s) for SSL/TLS
* Websocket for realtime alerts
* Webhooks for UniFi events, alarms and DPI data
* Flexibility of single service or microservice(s) deployment

## Upcoming Features ##
* Frontend with Bootstrap + Jinja2 Templates
* DPI analysis with AI
* NOC Dashboard 

### Poetry Init ###

* git clone 
* cd netifi_dash/FOLDER_NAME
* apt install python3.12-venv
* python3 -m venv .venv 
* . .venv/bin/activate
* pip install poetry 
* poetry install
* cd FOLDER_NAME/src/FOLDER_NAME
* poetry run python app.py

### If Not Using Poetry ###

* git clone 
* cd netifi_dash/FOLDER_NAME
* apt install python3.12-venv
* python3 -m venv .venv 
* . .venv/bin/activate
* pip install quart asyncio hypercorn pytest-asyncio websocket-client
* cd FOLDER_NAME/src/FOLDER_NAME/ 
* python3 app.py

### Production ###

* hypercorn app:app --bind '0.0.0.0:CUSTOM_PORT'




