import uuid
from util_models.PDF import PDF

class Session:

    def __init__(self, sess_name=''):
        self.session_name = sess_name
        self.id = self.gen_id()
        self.net_sess = []
        self.prtct_sess =[]
        self.accs_sess = []
        self.pdf = PDF()


    def gen_id(self):
        try:
            id = uuid.uuid4()
        except Exception as e:
            return {"status_msg": "ID Gen Failed",
                    "status_code": e}
        return str(id)

