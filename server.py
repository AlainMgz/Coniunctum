import socket
import threading
import json
from modules.get_ip import get_local_ip
from modules.block_validator import is_block_valid

HEADER = 64
PORT = 5050
SERVER = str(get_local_ip())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

print("[STARTING] Server is starting...")
start()