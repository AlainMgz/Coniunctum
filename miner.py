import hashlib
import json
import datetime
import os
import modules.chain_validation as chain_validation
from modules.get_ip import get_local_ip
from client import send_block
from modules.block_validator import is_chain_valid, is_block_valid

# Function to compute the proof of work for the next block
def proof_of_work(previous_block):
    difficulty = chain_validation.difficulty
    new_proof = 1
    check_proof = False
    while check_proof is False:
        hash_operation = hashlib.sha256(str(str(new_proof**2) + json.dumps(previous_block, sort_keys = True)).encode()).hexdigest()
        if hash_operation[:difficulty] == '0'*difficulty:
            check_proof = True
        else:
            new_proof += 1
    return new_proof

# Fucntion to broadcast the newly mined block to the network
def broadcast_block(block):
    ip_local = get_local_ip()
    with open('data/nodes.json') as nodes_file:
        nodes_data = json.load(nodes_file)
        for d in nodes_data['nodes']:
            if d != ip_local:
                try:
                    send_block(block, d)
                except ConnectionRefusedError:
                    pass
            else:
                pass

# Function that defines the mining process
def mine():
    # Getting the miner's wallet address
    try:
        with open('data/data.json') as datafile:
            data = json.load(datafile)
            for d in data['user_data']:
                node_address = d['wallet']           
    except FileNotFoundError:
        print("Missing 'data/data.json' file")
        quit()
    
    with open('data/blockchain.json') as chain_file:
        chain = json.load(chain_file)
    previous_block = chain[-1]
    proof = None
    proof = proof_of_work(previous_block)
    if proof:
        # Constructing the new block
        previous_hash = chain_validation.hash(previous_block)
        #with open("transactions_safe.json") as safe_tx_file:
        #   safe_tx = json.load(safe_tx_file)
        # ....
        transactions = []
        # Add miner reward transaction
        transactions.append({'type' : 'reward',
                             'receiver': node_address,
                             'amount': 10,})
        block = {'index': len(chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'miner': node_address,
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': transactions}
        transactions = []
        # Verify new block
        if is_block_valid(block, chain):
            # Add it to the blockchain and broadcast it to the network
            chain.append(block)
            with open('data/blockchain.json', 'w') as blockchain_file:
                json.dump(chain, blockchain_file)
            broadcast_block(block)
        else:
            pass
try:
    mine()
except KeyboardInterrupt:
    pass


