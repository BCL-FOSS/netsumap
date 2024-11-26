from quart import Quart
import nest_asyncio
import os
from models.RedisDB import RedisDB

app = Quart(__name__)
app.config.from_object("config")

folder_name = 'probe_data'
data_dir_path = os.path.join(app.instance_path, folder_name)

# General quart settings
app.config['MAX_CONTENT_LENGTH'] = 500 * 1000 * 1000  # 500 MB
app.config['PROBE_DATA_FOLDER'] = data_dir_path
app.config['CORS_HEADER'] = 'application/json'

nest_asyncio.apply()