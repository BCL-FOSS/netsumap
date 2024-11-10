"""
TCP Ping Test (defaults to port 80, 10000 packets)

Usage: ./tcpping.py host [port] [maxCount]
- Ctrl-C Exits with Results
"""

import sys
import socket
import time
import signal
from timeit import default_timer as timer

class Uptime:
    def __init__(self) -> None:
        # Required Host
        self.host = None
        self.count = 0
        # Pass/Fail counters
        self.passed = 0
        self.failed = 0
          
    def getResults(self):
        lRate = 0
        if self.failed != 0:
            lRate = self.failed / (self.count) * 100
            lRate = "%.2f" % lRate

        print("\nTCP Ping Results: Connections (Total/Pass/Fail): [{:}/{:}/{:}] (Failed: {:}%)".format((self.count), self.passed, self.failed, str(lRate)))

    def signal_handler(self, signal, frame):
        """ Catch Ctrl-C and Exit """
        self.getResults()
        
        sys.exit(0)

    def run(self, host='', port=0, maxCount=10000):
        # Register SIGINT Handler
        signal.signal(self, signal.SIGINT, self.signal_handler)

        # Loop while less than max count or until Ctrl-C caught
        while self.count < maxCount:
            self.host = host

            # Increment Counter
            self.count += 1

            success = False

            # New Socket
            s = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

            # 1sec Timeout
            s.settimeout(1)

            # Start a timer
            s_start = timer()

            # Try to Connect
            try:
                if int(port) != 0:
                    s.connect((self.host, int(port)))
                else:
                    s.connect(self.host)

                s.shutdown(socket.SHUT_RD)
                success = True
            
            # Connection Timed Out
            except socket.timeout:
                print("Connection timed out!")
                self.failed += 1
            except OSError as e:
                print("OS Error:", e)
                self.failed += 1
            finally:
                s.close()

            # Stop Timer
            s_stop = timer()
            s_runtime = "%.2f" % (1000 * (s_stop - s_start))

            if success:
                print("Connected to %s[%s]: tcp_seq=%s time=%s ms" % (self.host, port, (self.count-1), s_runtime))
                self.passed += 1

            # Sleep for 1sec
            if self.count < maxCount:
                time.sleep(1)

        # Output Results if maxCount reached
        self.getResults()