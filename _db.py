
import sqlite3, configparser
from collections import OrderedDict
from subprocess import check_output

config = configparser.ConfigParser()
config.read('config.ini')

db = sqlite3.connect('peering.db')
c = db.cursor()


class Peer:
    def find(where_clause='1=1'):
        return [Peer(p) for p in c.execute('select rowid,* from peers where '+where_clause)]

    def get_next_wg_listenport():
        item = c.execute('select max(wg_listenport)+1 from peers where vpn_type="wireguard"').fetchone()
        if item and item[0]:
            return item[0]
        else:
            return int(config['defaults']['wg_listenport'])

    def __init__(self, data=None):
        if data == None:
            self._id = None
        else:
            self._id, self.peername, self.asnumber, self.vpn_type, self.wg_listenport, self.wg_peer_endpoint, self.wg_peer_publickey, self.peer_ipv4, self.peer_ipv6, self.my_wg_privatekey, self.my_transfer_ipv4, self.my_transfer_ipv6 = data

    def get_ifname(self):
        if self.vpn_type == 'wireguard':
            if self.peername.startswith('$'):
                return 'wg_' + self.peername[1:]
            else:
                return 'wg_peer_' + self.peername

    def save(self):
        if self._id == None:
            c.execute('insert into peers values (?,?,?,?,?,?,?,?,?,?,?)',
                    (self.peername, self.asnumber, self.vpn_type, self.wg_listenport, self.wg_peer_endpoint, self.wg_peer_publickey, self.peer_ipv4, self.peer_ipv6, self.my_wg_privatekey, self.my_transfer_ipv4, self.my_transfer_ipv6))
        else:
            c.execute('update peers set peername = ?, asnumber = ?, vpn_type = ?, wg_listenport = ?, wg_peer_endpoint = ?, wg_peer_publickey = ?, peer_ipv4 = ?, peer_ipv6 = ?, my_wg_privatekey = ?, my_transfer_ipv4 = ?, my_transfer_ipv6 = ? where rowid = ?',
                    (self.peername, self.asnumber, self.vpn_type, self.wg_listenport, self.wg_peer_endpoint, self.wg_peer_publickey, self.peer_ipv4, self.peer_ipv6, self.my_wg_privatekey, self.my_transfer_ipv4, self.my_transfer_ipv6, self.rowid))
        db.commit()

    def get_obj(self):
        publish = ['peername', 'vpn_type', 'wg_listenport', 'wg_peer_endpoint', 'wg_peer_publickey', 'peer_ipv4', 'peer_ipv6', 'my_transfer_ipv4', 'my_transfer_ipv6']
        o = OrderedDict([(k, getattr(self, k)) for k in publish])
        o['my_wg_publickey'] = Peer.wg_pubkey(self.my_wg_privatekey)
        return o


    def wg_pubkey(privkey):
        return check_output(["wg", "pubkey"], input=privkey.encode("ascii")).decode("ascii").strip().strip()


