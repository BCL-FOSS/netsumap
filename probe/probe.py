#!/usr/bin/python

import sys
import sqlite3
import os
from utils.NetsumapCoreConn import NetsumapCoreConn
from utils.Network import Net

USE_DB=True

if os.path.exists('probe.db') == False:
    conn = sqlite3.connect('probe.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE pbdata(id, status, host_ip, hostname)")
    res = cur.execute("SELECT name FROM sqlite_master")
    if res.fetchone() is None:
        print('Failed to create table in db ')
        USE_DB=False
else:
     print("Probe DB already exists")

def main(url='', count=0):
    netmap = NetsumapCoreConn()
    network = Net()

    ports = network.open_tcp_ports()

    netmap.register(url=url, USE_DB=USE_DB, ports=ports)
    
    # network.net_scan(url=url, count=count)
    
if __name__ == "__main__":
    url = sys.argv[1]
    pcap_count = int(sys.argv[2])
    main(url=url, count=pcap_count)


    

