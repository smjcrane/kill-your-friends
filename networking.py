import re
import os

def mac_from_ip(ip):
    # Currently Windows only
    with os.popen('arp -a') as f:
        data = f.read()

    for line in re.findall('([-.0-9]+)\s+([-0-9a-f]{17})\s+(\w+)',data):
        if line[0] == ip:
            return line[1]

