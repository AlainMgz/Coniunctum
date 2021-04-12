import socket
import json

# Function to send block data to a server
def send_block(block, addr):
    HEADER = 64
    PORT = 56230
    FORMAT = 'utf-8'
    ADDR = (addr, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    block_se = json.dumps(block)
    block_msg = block_se.encode(FORMAT)
    msg_length = len(block_msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    # We first send the length of the message so that the server can then listen to exactly the right message size
    # We do that in all the following communication functions as well
    client.send(send_length)
    client.send(block_msg)
    print(client.recv(2048).decode(FORMAT))

# Function to request blockchain data from a server
def req_blockchain(addr):
    HEADER = 64
    PORT = 56230
    FORMAT = 'utf-8'
    ADDR = (addr, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    msg_length = len("REQBLOCKCHAIN")
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send("REQBLOCKCHAIN".encode(FORMAT))
    client.recv(2048).decode(FORMAT)

# Function to request nodes data from a server (this is for nodes discovery, as a node needs to know the other nodes of the network)
# So we retrieve the nodes list of the given node
def req_nodes(addr):
    HEADER = 64
    PORT = 56230
    FORMAT = 'utf-8'
    ADDR = (addr, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    msg_length = len("REQNODES")
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send("REQNODES".encode(FORMAT))
    print(client.recv(2048).decode(FORMAT))
    return True

# Function to send chain data to a server (is only called when the server gets a blockchain request from some node)
def send_chain(addr):
    HEADER = 64
    PORT = 56230
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
    client.recv(2048).decode(FORMAT)

# Function to send nodes data to a server (is only called when the server gets a nodes request from some node)
def send_nodes(addr):
    HEADER = 64
    PORT = 56230
    FORMAT = 'utf-8'
    ADDR = (addr, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    msg_length = len("NODES".encode(FORMAT))
    send_type_length = str(msg_length).encode(FORMAT)
    send_type_length += b' ' * (HEADER - len(send_type_length))
    client.send(send_type_length)
    client.send("NODES".encode(FORMAT))
    with open("data/nodes.json") as nodes_file:
        nodes = json.load(nodes_file)
    nodes_se = json.dumps(nodes)
    nodes_msg = nodes_se.encode(FORMAT)
    msg_length = len(nodes_msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(nodes_msg)
    print(client.recv(2048).decode(FORMAT))
