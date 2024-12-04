import os
import sqlite3
import uuid
import socket

class Probe:
    def __init__(self) -> None:
        pass

    def gen_probe_register_data(self):
        id=self.gen_id()
        probe_id="prb"+id
        hostname=socket.gethostname()

        if probe_id and hostname:
            return probe_id, hostname

    def gen_id(self):
        id = uuid.uuid4()
        if id:
            return str(id)
        else:
            return print("Probe ID Gen Failed")  
