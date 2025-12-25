#!/usr/bin/env python3

import can
bus = can.Bus(channel="can0", interface="socketcan")

for can_id in range(0x700, 0x800):
    isotp_request = [0x01, 0x64]
    if len(isotp_request) < 8:
        isotp_request += [0x00]*(8-len(isotp_request))
    msg = can.Message(arbitration_id=can_id, data=isotp_request, is_extended_id=False)
    bus.send(msg)
    response = bus.recv(0.5)
    if not response: 
        print(f"{hex(can_id)} no response")
        continue
    data = response.data
    print(f"{can_id} {data}")

bus.shutdown()
