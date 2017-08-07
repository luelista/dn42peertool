#!/usr/bin/env python3

from subprocess import check_call, check_output
from _db import Peer

for peer in Peer.find():
    iface = peer.get_ifname()
    try:
        out=check_output(['ping', '-c', '1', peer.peer_ipv4])
        v4_ok=True
    except:
        v4_ok=False
        print("FAIL: ",ex)
    try:
        if peer.peer_ipv6.startswith('fe80:'): peer.peer_ipv6 += '%' + iface
        check_output(['ping', '-c', '1', peer.peer_ipv6])
        v6_ok=True
    except Exception as ex:
        v6_ok=False
        print("FAIL: ",ex)
    print("Peer "+peer.peername+"   "+peer.peer_ipv4+" "+("success" if v4_ok else "fail")+"   "+peer.peer_ipv6+" "+("success" if v6_ok else "fail"))

