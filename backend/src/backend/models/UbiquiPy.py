import aiohttp
import uuid

class UbiquiPy:

    def __init__(self):
        self.id = ''
        self.name = ''
        self.ubiquipy_client_session = aiohttp.ClientSession()
            
    def gen_id(self):
        try:
            id = uuid.uuid4()
        except Exception as e:
            return {"status_msg": "ID Gen Failed",
                    "status_code": e}
        return str(id)