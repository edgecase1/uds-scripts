from scapy.all import *
from time import sleep
from datetime import datetime

conf.contribs['ISOTP'] = {'use-can-isotp-kernel-module': True}
conf.contribs['CANSocket'] = {'use-python-can': False}
load_contrib('cansocket')
load_contrib('isotp')
load_layer('can')
load_contrib('automotive.uds')

sock = ISOTPNativeSocket("can0", rx_id=0x7e8, tx_id=0x7e0, basecls=UDS, padding=True)

def request_seed():
    change_diagnostic_session_request = UDS()/UDS_DSC(diagnosticSessionType=0x3)
    response_change_session = sock.sr1(change_diagnostic_session_request, verbose=False)
    request_seed_security_access_0x3 = UDS()/UDS_SA(securityAccessType=0x3)
    response_seed = sock.sr1(request_seed_security_access_0x3, verbose=False)
    return response_seed.securitySeed

def get_key_algorithm(seed, pin):
    seed_int = int.from_bytes(seed, byteorder='big')
    key_int = seed_int + pin
    key_bytes = key_int.to_bytes(4, 'big')
    return key_bytes

def tester_present():
    tester_present_request = UDS()/UDS_TP()
    tester_present_response = sock.sr1(tester_present_request) # no response ...
    tester_present_response.show()
    
def change_diagnostic_session(diagSessType=0x01):
    change_diagnostic_session_request = UDS()/UDS_DSC(diagnosticSessionType=diagSessType) # Extended Diagnostic Session
    diagnostic_session_response = sock.sr1(change_diagnostic_session_request)
    diagnostic_session_response.show()
    print("sessionParameterRecord", diagnostic_session_response.sessionParameterRecord)

def security_access(pin):
    seed_security_access_request = UDS()/UDS_SA(securityAccessType=0x3)
    response_seed = sock.sr1(seed_security_access_request)
    response_seed.show()
    seed = response_seed.securitySeed
    print("securitySeed", seed)
    
    key = get_key_algorithm(seed, pin) # four bytes as a key
    print("key", key)
    security_access_sendkey = UDS()/UDS_SA(securityAccessType=0x4, securityKey=key)
    response_security_access = sock.sr1(security_access_sendkey)
    response_security_access.show()

def read_data_by_id(did):
    rdbi_pkt = UDS()/UDS_RDBI(identifiers=[did])
    sock.send(rdbi_pkt)
    rx = sock.recv()
    if rx: rx.show()


def reset(resetType):
    reset = UDS()/UDS_ER(resetType=1)
    reset_resp = sock.sr1(reset)
    reset_resp.show()

pin = 27971


tester_present()
change_diagnostic_session(0x03)
tester_present()
seed_security_access_request = UDS()/UDS_SA(securityAccessType=0x1)
response_seed = sock.sr1(seed_security_access_request)
response_seed.show()
if request_seed.haslayer(UDS_NRC):
    print("error")
else:
    seed = response_seed.securitySeed
    print("securitySeed", seed)
#read_data_by_id(0xf190)
#security_access(pin)
reset(1)
