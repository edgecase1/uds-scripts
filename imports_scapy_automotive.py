#!/usr/bin/env python3

from scapy.all import *
conf.contribs['CANSocket'] = {'use-python-can': False}
conf.contribs['ISOTP'] = {'use-can-isotp-kernel-module': True}
load_contrib('cansocket')
load_contrib('automotive.uds')
load_contrib('isotp')
load_contrib('can')
from scapy.contrib.automotive.uds_scan import *

