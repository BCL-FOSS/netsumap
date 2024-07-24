# NetiFi Dash #

## Experimental Webapp for UbiquiPy Automation Framework ##

[UbiquiPy Repo](https://github.com/BCL-FOSS/UbiquiPy-UniFi-Automation)
[Learn more about UbiquiPy here](https://www.baughcl.com/ubiquipy.html)
* Flask: Webhooks, front end with Flask Templates & Jinja2, Backend API
* SocketIO: Web socket  
* This is a repo mainly for learning and experimentation, though there are plans to push this into production in the future.

### Environment Initialization ###

Initialization procedures for testing and production.

* git clone 
* cd netifi_dash
* cd frontend / cd backend
* apt install python3.10-venv
* python3 -m venv .venv 
* . .venv/bin/activate
* pip install Flask requests Faker Flask-SocketIO redis


### Testing ###

* flask run -p 3000 --host=0.0.0.0
* or
* flask run --host=0.0.0.0

### Production ###

* gunicorn -w 2 -b 0.0.0.0:3000 myapp:app

