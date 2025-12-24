

from scapy.all import *
conf.contribs['CANSocket'] = {'use-python-can': False}
conf.contribs['ISOTP'] = {'use-can-isotp-kernel-module': True}
load_contrib('cansocket')
load_contrib('automotive.uds')
load_contrib('isotp')
load_contrib('can')
from scapy.contrib.automotive.uds_scan import *

def check_rdbi(did):
    sock = ISOTPSocket(iface="can0", tx_id=0x7e0, rx_id=0x7e8, basecls=UDS, padding=True)
    req = UDS()/UDS_RDBI(identifiers=[did])
    sock.send(req)
    resp = sock.recv()
    if resp.haslayer(UDS) and resp[UDS].service == 0x7F:
        return None
    else:
        return resp.load

for did in range(0xf100,0xffff):
    data = check_rdbi(did)
    if data:
        print(hex(did), data)
