#!/bin/bash
#
#
set -o errexit

perror()
{
	echo $* >&2
	exit 1
}

ip link show dev can0 >/dev/null || perror "interface can0 not found"

ip link set down dev can0
ip link set up dev can0 type can bitrate 500000

ip link show dev can0
