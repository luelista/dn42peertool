#!/usr/bin/env python3
import logging
logging.basicConfig(level='INFO')
import json
from _db import Peer, config

json={}
json['peername'] = input("Peer Name: ")
json['asnumber'] = input("AS Number: ")
json['wg_peer_endpoint'] = input("Peer Wireguard Endpoint (host:port): ")
json['wg_peer_publickey'] = input("Peer Public Key: ")
json['peer_ipv4'] = input("Peer Transit IPv4:")
json['peer_ipv6'] = input("Peer Transit IPv6:")


peer = Peer()
peer.peername = json['peername']
peer.vpn_type = 'wireguard' #json['vpn_type']
peer.asnumber = ''
peer.wg_listenport = Peer.get_next_wg_listenport()
peer.wg_peer_endpoint = json['wg_peer_endpoint']
peer.wg_peer_publickey = json['wg_peer_publickey']
peer.peer_ipv4 = json['peer_ipv4']
peer.peer_ipv6 = json['peer_ipv6']
peer.my_transfer_ipv4 = config['defaults']['my_transfer_ipv4']
peer.my_transfer_ipv6 = config['defaults']['my_transfer_ipv6']
peer.my_wg_privatekey = config['defaults']['my_wg_privatekey']
peer.save()





