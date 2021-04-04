import socket
import threading
import json
from modules.get_ip import get_local_ip
from modules.block_validator import is_block_valid
from modules.chain_validation import is_chain_valid, hash
from client import send_chain

HEADER = 64
PORT = 5050
SERVER = str(get_local_ip())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

def handle_client(conn, addr):
    connected = True

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)

        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False

            elif msg == "REQBLOCKCHAIN":
                print(f"Blockchain request from {addr}")
                addr_s = addr[0]
                conn.send("Chain successfully requested.".encode(FORMAT))
                send_chain(addr_s)
                connected = False

            elif msg == "BLOCKCHAIN":
                print(f"Blockchain received from {addr}")
                chain_length = conn.recv(HEADER).decode(FORMAT)

                if chain_length:
                    chain_length = int(chain_length)
                    chain_received = ""
                    bytes_recvd = 0
                    while bytes_recvd < chain_length:
                        chain_recv = conn.recv(min(chain_length - bytes_recvd, 2048))
                        chain_received = chain_received + chain_recv.decode(FORMAT)
                        bytes_recvd = bytes_recvd + len(chain_recv.decode(FORMAT))
                    chain = chain_received
                    chain_dict = json.loads(chain)
                    print(chain_dict[-1])
                    chain_is_valid = is_chain_valid(chain_dict)
                    if chain_is_valid:
                        try:
                            with open("data/blockchain.json") as og_chain_file:
                                og_chain = json.load(og_chain_file)
                            if og_chain == chain_dict:
                                conn.send("Same".encode(FORMAT))
                                return "Same"
                            else:
                                if og_chain[-1]['index'] < chain_dict[-1]['index']:
                                    with open("data/blockchain.json", "w") as chain_file:
                                        json.dump(chain_dict, chain_file)
                                    conn.send("Chain successfully broadcasted.".encode(FORMAT))
                                    return "Blockchian updated"
                                else:
                                    conn.send("Same or newer".encode(FORMAT))
                                    return "Same or newer"
                        except FileNotFoundError:
                            conn.send("Blockchain data file missing".encode(FORMAT))
                            return "Blockchain data file missing"
                    else:
                        err = {'message' : 'Received chain is not valid !',
                               'ip_sender': addr[0]}
                        conn.send(json.dumps(err).encode(FORMAT))
                        return err


            else:
                msg_dict = json.loads(msg)
                print(f"Block from {addr} | Timestamp : {msg_dict['timestamp']} | Index : {msg_dict['index']}")
                
                try:
                    with open("data/blockchain.json") as chain_file:
                        chain = json.load(chain_file)

                    msg_is_valid = is_block_valid(json.loads(msg), chain)
                    
                    if msg_is_valid:
                        try:
                            chain.append(json.loads(msg))
                        except AttributeError:
                            pass
                        
                        with open("data/blockchain.json", "w") as chain_file:
                            json.dump(chain, chain_file)
                        conn.send("Block successfully broadcasted.".encode(FORMAT))
                        return json.loads(msg)

                    else:
                        err = {'message' : 'Received block is not valid !',
                               'ip_sender': addr[0]}
                        conn.send(json.dumps(err).encode(FORMAT))
                        return err

                except FileNotFoundError:
                        return "Blockchain data file missing"

            

    conn.close()

def start(stop):
    server.listen()
    print("[STARTING] Server is starting...")
    print(f"[LISTENING] Server is listening on {SERVER}\n")
    while True:
        if stop():
            break
        conn, addr = server.accept()
        listening = threading.Thread(target=handle_client, args=(conn, addr))
        listening.start()

