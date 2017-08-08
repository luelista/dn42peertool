
import sqlite3, configparser

config = configparser.ConfigParser()
config.read('config.ini')

db = sqlite3.connect('peering.db')
c = db.cursor()


class Peer:
    def find(where_clause='1=1'):
        return [Peer(p) for p in c.execute('select rowid,* from peers where '+where_clause)]

    def get_next_wg_listenport(self):
        c.execute('select max(wg_listenport)+1 from peers where vpn_type="wireguard"')

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
            c.execute('insert into peers (?,?,?,?,?,?,?,?,?,?,?)',
                    (self.peername, self.asnumber, self.vpn_type, self.wg_listenport, self.wg_peer_endpoint, self.wg_peer_publickey, self.peer_ipv4, self.peer_ipv6, self.my_wg_privatekey, self.my_transfer_ipv4, self.my_transfer_ipv6))
        else:
            c.execute('update peers set peername = ?, asnumber = ?, vpn_type = ?, wg_listenport = ?, wg_peer_endpoint = ?, wg_peer_publickey = ?, peer_ipv4 = ?, peer_ipv6 = ?, my_wg_privatekey = ?, my_transfer_ipv4 = ?, my_transfer_ipv6 = ? where rowid = ?',
                    (self.peername, self.asnumber, self.vpn_type, self.wg_listenport, self.wg_peer_endpoint, self.wg_peer_publickey, self.peer_ipv4, self.peer_ipv6, self.my_wg_privatekey, self.my_transfer_ipv4, self.my_transfer_ipv6, self.rowid))



