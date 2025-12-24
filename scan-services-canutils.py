#!/usr/bin/env python3

import can

bus = can.Bus(channel="can0", interface="socketcan")
bus.set_filters([
	{"can_id": 0x7e4, "can_mask": 0x1FFF, "extended": False},
	{"can_id": 0x7ec, "can_mask": 0x1FFF, "extended": False}
])

UDS_NRC = {
    0x10: "General Reject",
    0x11: "Service Not Supported",
    0x12: "Sub-Function Not Supported",
    0x13: "Incorrect Message Length or Invalid Format",
    0x14: "Response Too Long",
    0x21: "Busy Repeat Request",
    0x22: "Conditions Not Correct",
    0x24: "Request Sequence Error"
    }

isotp_header = 0x02 # single frame 2 bytes
for service in range(0x00, 0x38):
    # service = 0x11
    service_parameter = [0x01]
    isotp_service_request = [isotp_header, service] + service_parameter
    if len(isotp_service_request) < 8:
        isotp_service_request += [0xCC]*(8-len(isotp_service_request))
    msg = can.Message(arbitration_id=0x7E4, data=isotp_service_request, is_extended_id=False)
    bus.send(msg)
    response = bus.recv(1)
    if not response: 
        print(f"{hex(service)} no response")
        continue
    data = response.data
    if data[1] == service+0x40:
        print(f"{hex(service)} positive response")
    elif data[1] == 0x7f and data[2] == service: # Negative Response
        nrc = data[3]
        if nrc in UDS_NRC.keys():
            nrc_desc = UDS_NRC[nrc]
        else:
            nrc_desc = f"0x{nrc:02X}"
        print(f"{hex(service)} negative response {nrc_desc}")
    else:
        print(f"{hex(service)} unexpected {data.hex()}")
    #print(response)

bus.shutdown()
