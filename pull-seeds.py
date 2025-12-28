from scapy.all import *
from time import sleep
from datetime import datetime

conf.contribs['ISOTP'] = {'use-can-isotp-kernel-module': True}
conf.contribs['CANSocket'] = {'use-python-can': False}
load_contrib('cansocket')
load_contrib('isotp')
load_layer('can')
load_contrib('automotive.uds')
from scapy.contrib.automotive.uds_scan import *

sock = ISOTPNativeSocket("can0", rx_id=0x7ec, tx_id=0x7e4, basecls=UDS, padding=True)
sock_can = CANSocket("can0", basecls=CAN, padding=True)

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
    if diagnostic_session_response[UDS].service == 0x7F:
        print("NegativeResponse")
        return None
    print("sessionParameterRecord", diagnostic_session_response.sessionParameterRecord)
    return diagnostic_session_response.sessionParameterRecord

def security_access(level):
    seed_security_access_request = UDS()/UDS_SA(securityAccessType=level)
    response_seed = sock.sr1(seed_security_access_request)
    response_seed.show()
    seed = response_seed.securitySeed
    print(f"securitySeed {seed.hex()}")

def xxx():
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

def read_mem():
    req = UDS()/UDS_RMBA(memoryAddress1=0x400000, memorySize1=0x100)
    sock.send(req)
    resp = sock.recv()
    resp.show()

def reset(resetType):
    print("reset")
    reset = UDS()/UDS_ER(resetType=1)
    reset_resp = sock.sr1(reset)
    reset_resp.show()

pin = 27971

def main():
    reset(1)
    frame = sock_can.recv() # wait for a CAN frame
    frame.show()
    #time.sleep(0.01)
    #tester_present()
    change_diagnostic_session(0x2)
    #tester_present()
    #security_access(0x1)
    #if request_seed.haslayer(UDS_NRC):
    #    print("error")
    #else:
    #    seed = response_seed.securitySeed
    #    print("securitySeed", seed)
    #read_data_by_id(0xf190)
    #security_access(pin)

main()
