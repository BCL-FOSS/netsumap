from quart import Quart
import nest_asyncio
import sqlite3
import os

app = Quart(__name__)
app.config.from_object("config")

# Probe data folder settings
folder_name = 'probe_data'
data_dir_path = os.path.join(app.instance_path, folder_name)

# General quart settings
app.config['MAX_CONTENT_LENGTH'] = 500 * 1000 * 1000  # 500 MB
app.config['PROBE_DATA_FOLDER'] = data_dir_path
app.config['CORS_HEADER'] = 'application/json'

# Probe DB settings
db_path = os.path.join(app.config['PROBE_DATA_FOLDER'], 'probe.db')
app.config['DB_PATH'] = db_path

nest_asyncio.apply()