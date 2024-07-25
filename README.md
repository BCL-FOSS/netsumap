# NetiFi Dash #

## Experimental, Webapp for UbiquiPy Automation Framework ##

* [UbiquiPy Repo](https://github.com/BCL-FOSS/UbiquiPy-UniFi-Automation)
* [Learn more about UbiquiPy here](https://www.baughcl.com/ubiquipy.html) 
* This is a repo mainly for learning and experimentation, though there are plans to push this into production in the near future.
* Quart for async calls
* Caddy reverse proxy(s) for SSL/TLS

## Upcoming Features ##
* Websocket 
* Backend API + Webhook
* Frontend with Bootstrap + Jinja2 Templates

### Websocket ###

#### Init ####

* git clone 
* cd netifi_dash/socket
* apt install python3.10-venv
* python3 -m venv .venv 
* . .venv/bin/activate
* pip install poetry 
* poetry install
* cd /src/socket/
* poetry run python app.py

##### If Not Using Poetry #####

* pip install quart asyncio hypercorn pytest-asyncio
* cd /src/socket/
* python3 app.py

#### Production ####

* hypercorn app:app

### Backend + Webhook, Frontend ###

#### Init ####

* git clone 
* cd netifi_dash/
* apt install python3.10-venv
* python3 -m venv .venv 
* . .venv/bin/activate
* pip install Flask requests Faker waitress

#### Production ####

* waitress-serve --host 127.0.0.1 app:app





