import socket
import threading
import json
from modules.get_ip import get_local_ip
from modules.block_validator import is_block_valid
from modules.chain_validation import is_chain_valid, hash
from client import send_chain, send_nodes

# Function called in a separate thread that handles incoming connections to the server
def handle_client(conn, addr):
    HEADER = 64
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"
    connected = True
    ip_local = get_local_ip()

    while connected:
        # Listening to the length of the message incoming
        msg_length = conn.recv(HEADER).decode(FORMAT)

        if msg_length:
            msg_length = int(msg_length)
            # Listening to the actual message
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False

            elif msg == "REQBLOCKCHAIN":
                addr_s = addr[0]
                conn.send("Chain successfully requested.".encode(FORMAT))
                # Call for the send_chain function of the TCP client to send chain data
                send_chain(addr_s)
                return f"Blockchain request from {addr}"

            elif msg == "REQNODES":
                addr_s = addr[0]
                try:
                    # We add the IP addr that requested the nodes to our nodes list, as the request most definetely comes from a newly setup node
                    with open("data/nodes.json") as nodes_file:
                        nodes = json.load(nodes_file)
                    nodes['nodes'].append(addr_s)
                    # We remove any duplicates
                    nodes['nodes'] = list(dict.fromkeys(nodes['nodes']))
                    # And dump the nodes list containing the new one in the local nodes file
                    with open("data/nodes.json", "w") as nodes_file:
                        json.dump(nodes, nodes_file)
                except FileNotFoundError:
                    return "Missing data/nodes.json file"
                conn.send("Nodes successfully requested.".encode(FORMAT))
                # Call for the send_nodes function of the TCP client to send nodes data
                send_nodes(addr_s)
                return f"Nodes list request from {addr}"

            elif msg == "BLOCKCHAIN":
                #print(f"Blockchain received from {addr}")
                # Listen for the length of the chain incoming
                chain_length = conn.recv(HEADER).decode(FORMAT)

                if chain_length:
                    chain_length = int(chain_length)
                    # We loop until we receive the entire chain message
                    chain_received = ""
                    bytes_recvd = 0
                    while bytes_recvd < chain_length:
                        chain_recv = conn.recv(min(chain_length - bytes_recvd, 2048))
                        chain_received = chain_received + chain_recv.decode(FORMAT)
                        bytes_recvd = bytes_recvd + len(chain_recv.decode(FORMAT))
                    chain = chain_received
                    try:
                        chain_dict = json.loads(chain)
                    except json.decoder.JSONDecodeError:
                        return "Corrupted blockchain data..."
                    #print(chain_dict[-1])
                    # Verifying the chain
                    chain_is_valid = is_chain_valid(chain_dict)
                    if chain_is_valid:
                        try:
                            # We compare the received chain with our local one (if we have a local one, otherwise we just dump the received one in a file)
                            with open("data/blockchain.json") as og_chain_file:
                                og_chain = json.load(og_chain_file)
                            if og_chain == chain_dict:
                                conn.send("Same".encode(FORMAT))
                                return "Same"
                            else:
                                if og_chain[-1]['index'] < chain_dict[-1]['index']:
                                    with open("data/blockchain.json", "w") as chain_file:
                                        json.dump(chain_dict, chain_file)
                                    # We only replace our local blockchain if the received one is strictly longer than our own
                                    conn.send("Chain successfully broadcasted.".encode(FORMAT))
                                    return "Blockchain updated"
                                else:
                                    conn.send("Same or newer".encode(FORMAT))
                                    return "Same or newer"
                        except FileNotFoundError:
                            with open("data/blockchain.json", "w") as chain_file:
                                json.dump(chain_dict, chain_file)
                            conn.send("Chain successfully broadcasted.".encode(FORMAT))
                            return "Blockchain updated"
                    else:
                        err = {'message' : 'Received chain is not valid !',
                               'ip_sender': ip_local}
                        conn.send(json.dumps(err).encode(FORMAT))
                        return err

            elif msg == "NODES":
                # More or less the same as with receiving chain data
                print(f"Nodes received from {addr}")
                nodes_length = conn.recv(HEADER).decode(FORMAT)

                if nodes_length:
                    nodes_length = int(nodes_length)
                    nodes_received = ""
                    bytes_recvd = 0
                    while bytes_recvd < nodes_length:
                        nodes_recv = conn.recv(min(nodes_length - bytes_recvd, 2048))
                        nodes_received = nodes_received + nodes_recv.decode(FORMAT)
                        bytes_recvd = bytes_recvd + len(nodes_recv.decode(FORMAT))
                    nodes = nodes_received
                    try:
                        nodes_dict = json.loads(nodes)
                    except json.decoder.JSONDecodeError:
                        return "Corrupted node data..."
                    are_nodes_valid = True 
                    if are_nodes_valid:
                        # We seperate two cases :
                        # One where we already have a nodes file and we just want to update it
                        # One where we don't have one so we directly dump the received nodes data in a file
                        try:
                            with open("data/nodes.json") as og_nodes_file:
                                og_nodes = json.load(og_nodes_file)
                            nodes_list = []
                            for i in range(len(og_nodes['nodes'])):
                                nodes_list.append(og_nodes['nodes'][i])
                            for i in range(len(nodes_dict['nodes'])):
                                nodes_list.append(nodes_dict['nodes'][i])
                            nodes_list = list(dict.fromkeys(nodes_list))
                            nodes_final = {}
                            nodes_final['nodes'] = []
                            for i in range(len(nodes_list)):
                                nodes_final['nodes'].append(nodes_list[i])
                            with open("data/nodes.json", "w") as nodes_file:
                                json.dump(nodes_final, nodes_file)
                            conn.send("Nodes successfully broadcasted.".encode(FORMAT))
                        except FileNotFoundError:
                            nodes_list = []
                            for i in range(len(nodes_dict['nodes'])):
                                nodes_list.append(nodes_dict['nodes'][i])
                            nodes_list = list(dict.fromkeys(nodes_list))
                            nodes_final = {}
                            nodes_final['nodes'] = []
                            for i in range(len(nodes_list)):
                                nodes_final['nodes'].append(nodes_list[i])
                            with open("data/nodes.json", "w") as nodes_file:
                                json.dump(nodes_final, nodes_file)
                            conn.send("Nodes successfully broadcasted.".encode(FORMAT))
                    else:
                        err = {'message' : 'Received chain is not valid !',
                               'ip_sender': ip_local}
                        conn.send(json.dumps(err).encode(FORMAT))
                        return err

            # This is for receiving block data (i.e when receiving a newly mined block)
            else:
                try:
                    msg_dict = json.loads(msg)
                except json.decoder.JSONDecodeError:
                    return "Corrupted block data..."
                print(f"\nBlock from {addr} | Timestamp : {msg_dict['timestamp']} | Index : {msg_dict['index']}")
                try:
                    with open("data/blockchain.json") as chain_file:
                        chain = json.load(chain_file)
                    # We verify if the received block is valid
                    msg_is_valid = is_block_valid(json.loads(msg), chain)
                    if msg_is_valid:
                        try:
                            # We append the valid block in our chain
                            chain.append(json.loads(msg))
                        except AttributeError:
                            pass
                        # We dump the new chain in our local file
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

# Function that starts the server (i.e makes it listen for incoming connections)
def start(server, SERVER):
    server.listen()
    print("[STARTING] Server is starting...")
    print(f"[LISTENING] Server is listening on {SERVER}\n")
    while True:
        # When a new connection arrives we send it in a parallel thread with the function defined above
        conn, addr = server.accept()
        listening = threading.Thread(target=handle_client, args=(conn, addr))
        listening.start()

