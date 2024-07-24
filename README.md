# NetiFi Dash #

## Experimental Webapp for UbiquiPy Automation Framework ##

* [UbiquiPy Repo](https://github.com/BCL-FOSS/UbiquiPy-UniFi-Automation)
* [Learn more about UbiquiPy here](https://www.baughcl.com/ubiquipy.html) 
* This is a repo mainly for learning and experimentation, though there are plans to push this into production in the near future.

## Upcoming Features ##
* Async Websocket 
* * Behind Caddy Reverse Proxy
* Async Backend
* Frontend with Flask/Jinja Templates

### Asynchronous, Secure Websocket ###

#### Environment Initialization ####

* git clone 
* cd netifi_dash/async_websocket
* apt install python3.10-venv
* python3 -m venv .venv 
* . .venv/bin/activate
* pip install quart asyncio hypercorn pytest-asyncio

#### Production ####

* hypercorn app:app

### Backend, Frontend, Webhook ###

#### Environment Initialization ####

* git clone 
* cd netifi_dash/
* apt install python3.10-venv
* python3 -m venv .venv 
* . .venv/bin/activate
* pip install Flask requests Faker waitress

#### Production ####

* waitress-serve --host 127.0.0.1 hello:app





