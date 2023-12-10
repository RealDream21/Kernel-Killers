"""from python_wireguard import Client, ServerConnection

local_ip = "192.168.100.2/24"
private = "S72aqA3SUpxEqZUM4OMw9g3cOXxRM7WQtz9UQVXd4CM="
client = Client("wg-client", private, local_ip)

srv_key = "DgLZYTtvqVkvt/TpOhfmZ8Pu+P5xrDj5Qlpnj+wEjU8="
endpoint = "34.155.214.0"
port = "51820"

server_conn = ServerConnection(srv_key, endpoint, port)

client.set_server(server_conn)
client.connect()
"""

from wireguard import Peer

peer = Peer('my-client', '192.168.24.0/24', address='192.168.24.45')

# Write out the peer config to the default location: /etc/wireguard/wg0.conf
peer.config.write()