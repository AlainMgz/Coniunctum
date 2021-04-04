import socket
import json

def send_block(block, addr):
    HEADER = 64
    PORT = 5050
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"
    ADDR = (addr, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    block_se = json.dumps(block)
    block_msg = block_se.encode(FORMAT)
    msg_length = len(block_msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(block_msg)
    print(client.recv(2048).decode(FORMAT))

def req_blockchain(addr):
    HEADER = 64
    PORT = 5050
    FORMAT = 'utf-8'
    ADDR = (addr, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)


    msg_length = len("REQBLOCKCHAIN")
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send("REQBLOCKCHAIN".encode(FORMAT))
    print(client.recv(2048).decode(FORMAT))

def send_chain( addr):
    HEADER = 64
    PORT = 5050
    FORMAT = 'utf-8'
    ADDR = (addr, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    msg_length = len("BLOCKCHAIN".encode(FORMAT))
    send_type_length = str(msg_length).encode(FORMAT)
    send_type_length += b' ' * (HEADER - len(send_type_length))
    client.send(send_type_length)
    client.send("BLOCKCHAIN".encode(FORMAT))
    with open("data/blockchain.json") as chain_file:
        chain = json.load(chain_file)
    chain_se = json.dumps(chain)
    chain_msg = chain_se.encode(FORMAT)
    msg_length = len(chain_msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(chain_msg)
    print(client.recv(2048).decode(FORMAT))
