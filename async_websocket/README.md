# NetiFi Dash WebSocket#

## Asynchronous, Secure Websocket for UbiquiPy data ##

* [UbiquiPy Repo](https://github.com/BCL-FOSS/UbiquiPy-UniFi-Automation)
* [Learn more about UbiquiPy here](https://www.baughcl.com/ubiquipy.html)

### Environment Initialization ###

* git clone 
* cd netifi_dash/async_websocket
* apt install python3.10-venv
* python3 -m venv .venv 
* . .venv/bin/activate
* pip install quart asyncio hypercorn pytest-asyncio

### Production ###

* hypercorn app:app

