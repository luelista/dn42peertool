#!/usr/bin/env python3

from subprocess import check_call, check_output
from ._db import Peer

ALL_IPS="::/0,0.0.0.0/0"
for peer in Peer.find('vpn_type="wireguard"'):
    print("Setting up "+peer.get_ifname()+", listen on "+str(peer.my_listenport)+", endpoint "+peer.peer_ep)
    try:
        try:
            check_output(["ip", "link", "delete", "dev", peer.get_ifname()])
        except:
            pass

        check_call(["ip", "link", "add", "dev", peer.get_ifname(), "type", "wireguard"])
        params = ["wg", "set", peer.get_ifname(),
            "listen-port", str(peer.my_listenport),
            "private-key", "/dev/stdin",
            "peer", peer.peer_pk,
            "endpoint", peer.peer_ep,
            "allowed-ips", ALL_IPS]
        check_output(params, input=peer.my_sk.encode('ascii'))
        check_call(["ip", "link", "set", "dev", peer.get_ifname(), "up"])
        check_call(["ip", "address", "add", peer.my_v4, "dev", peer.get_ifname(), "peer", peer.peer_v4])
        check_call(["ip", "-6", "address", "add", peer.my_v6, "dev", peer.get_ifname()])
        check_call(["ip", "-6", "route", "add", peer.peer_v6, "dev", peer.get_ifname()])
    except Exception as e:
        print("FAIL: ",e)
        check_call(["ip", "link", "delete", "dev", peer.get_ifname()])



