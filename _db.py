
import sqlite3

db = sqlite3.connect('peering.db')
c = db.cursor()


class Peer:
    def find(where_clause='1=1'):
        return [Peer(p) for p in c.execute('select * from peers where '+where_clause)]

    def __init__(self, data):
        self.peername, self.asnumber, self.vpn_type, self.wg_listenport, self.wg_peer_endpoint, self.wg_peer_publickey, self.peer_ipv4, self.peer_ipv6, self.my_wg_privatekey, self.my_transfer_ipv4, self.my_transfer_ipv6 = data

    def get_ifname(self):
        if self.vpn_type == 'wireguard':
            return 'wg_peer_' + self.peername



