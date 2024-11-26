import os
import sqlite3
import uuid
import socket

class Probe:
    def __init__(self) -> None:
        pass

    async def gen_probe_register_data(self):
        id=self.gen_id()
        probe_id="nmp"+id
        hostname=socket.gethostname()

        if probe_id and hostname:
            return probe_id, hostname

    async def create_probe_dir(self, data_dir_path=""):
        # Create probe data folder 
        if os.path.isdir(data_dir_path) is False:
            if os.makedirs(data_dir_path, exist_ok=True) == True:
                print(f"Probe data directory {data_dir_path} created successfully", flush=True)
                return True
            else:
                print(f"Probe data directory {data_dir_path} creation failed", flush=True)
                return False
        else:
            pass

    def gen_id(self):
        id = uuid.uuid4()
        if id:
            return str(id)
        else:
            return print("Probe ID Gen Failed")  
