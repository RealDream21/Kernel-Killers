import subprocess


number_of_clients = 0

class vpn_client():
    PrivateKey = None
    PublicKey = None
    Address = None
    isAvailable = None 
    def __init__(self, privkey, pubkey, address, isAvailable = True):
        self.PrivateKey = privkey
        self.PublicKey = pubkey
        self.Address = address
        self.isAvailable = isAvailable
        global number_of_clients
        number_of_clients += 1


def create_clients():
    global number_of_clients
    clients = []
    for i in range(0, 5):
        privkey = subprocess.check_output(["wg", "genkey"]).decode("utf-8").strip()
        pubkey = subprocess.check_output(["wg", "pubkey"], input=privkey.encode("utf-8")).decode("utf-8").strip()
        address = "192.168.10" + str(i) +".2/24"
        clients.append(vpn_client(privkey, pubkey, address))
    return clients

def main():
    writeFile = open("wg0.conf", "w")
    clients = create_clients()
    for client in clients:
        writeFile.write("[Peer]\n")
        writeFile.write(f"PublicKey = {client.PublicKey}\n")
        writeFile.write(f"AllowedIPs = {client.Address}\n")
        writeFile.write("\n")
    writeFile.close()
        
main()
