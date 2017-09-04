#!/usr/bin/env python3

from subprocess import check_call, check_output, DEVNULL
from _db import Peer, c

def delete_link(ifname):
    check_output(["ip", "link", "delete", "dev", ifname], stderr=DEVNULL)

ALL_IPS="::/0,0.0.0.0/0"
def create_wireguard_link(ifname, listen_port, private_key, peer_pk, peer_ep, allowed_ips=ALL_IPS):
    check_call(["ip", "link", "add", "dev", ifname, "type", "wireguard"])
    check_output(["wg", "set", ifname,
        "listen-port", str(listen_port),
        "private-key", "/dev/stdin",
        "peer", peer_pk,]+
        (["endpoint", peer_ep,] if peer_ep else [])+
        ["allowed-ips", allowed_ips], input=private_key.encode('ascii'))
    check_call(["ip", "link", "set", "dev", ifname, "up"])

def add_address(ifname, address, peer_address=None):
    cmd = ["ip", "address", "add", address, "dev", ifname]
    if peer_address: cmd += ["peer", peer_address]
    check_call(cmd)

for peer in Peer.find('vpn_type="wireguard"'):
    print("Setting up "+peer.get_ifname()+", listen on "+str(peer.wg_listenport)+", endpoint "+str(peer.wg_peer_endpoint))
    try:
        try:
            delete_link(peer.get_ifname())
        except:
            pass

        create_wireguard_link(peer.get_ifname(), peer.wg_listenport, peer.my_wg_privatekey, peer.wg_peer_publickey, peer.wg_peer_endpoint)
        if peer.my_transfer_ipv4: add_address(peer.get_ifname(), peer.my_transfer_ipv4, peer_address=peer.peer_ipv4)
        add_address(peer.get_ifname(), peer.my_transfer_ipv6, peer_address=peer.peer_ipv6)
    except Exception as e:
        print("FAIL: ",e)
        delete_link(peer.get_ifname())


