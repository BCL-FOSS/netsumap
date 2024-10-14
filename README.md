# net-con.ai #

## Threat Management & Network Automation Platform ##
### EXPERIMENTAL ###

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
* pip install quart asyncio hypercorn pytest-asyncio websocket-client requests ipython fpdf2
* cd FOLDER_NAME/src/FOLDER_NAME/ 
* python3 app.py

### Production ###

* hypercorn app:app --bind '0.0.0.0:CUSTOM_PORT'

##### Backend #####
* hypercorn app:app --bind '0.0.0.0:25000'

##### Websocket #####
* hypercorn app:app --bind '0.0.0.0:30000'

##### Frontend #####
* hypercorn app:app --bind '0.0.0.0:20000'






