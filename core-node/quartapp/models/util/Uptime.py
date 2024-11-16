from scapy.all import *
from scapy import *
from scapy.tools import *
from scapy.layers.inet import *

class Uptime:
    def __init__(self) -> None:
        # Required Host
        self.host = None
        self.count = 0
        # Pass/Fail counters
        self.passed = 0
        self.failed = 0

    def check_service(self, host='', port_list=[]):
       check_result = sr(IP(dst=host)/TCP(dport=port_list),inter=0.5,retry=-2,timeout=1)

   