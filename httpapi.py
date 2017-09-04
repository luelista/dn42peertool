#!/usr/bin/env python3
import logging
logging.basicConfig(level='INFO')
import json
from _db import Peer, config
from http.server import BaseHTTPRequestHandler, HTTPServer

class ApiHttpHandler(BaseHTTPRequestHandler):

    def jsonerror(self, err_code, err_msg):
        self.send_response(err_code)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'error': err_code, 'response': err_msg}).encode('utf-8'))

    def jsonresponse(self, answer):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps(answer).encode('utf-8'))

    def get_json_request(self):
        instr = self.rfile.read(int(self.headers['Content-Length']))
        return json.loads(instr.decode('utf-8'))

    def do_GET(self):
        if self.path == '/peers':
            peers = [p.get_obj() for p in Peer.find()]
            self.jsonresponse({'peers': peers})
        else:
            self.jsonerror(404, 'not found')

    def do_POST(self):
        if self.path == '/peers':
            peer = Peer()
            json = self.get_json_request()
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



listen_tupel = ('', int(config['httpapi']['listen_port']))
logging.info("Listening on %s", listen_tupel)
server = HTTPServer(listen_tupel, ApiHttpHandler)
server.serve_forever()


