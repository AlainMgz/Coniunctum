import hashlib
import json
import datetime
import os
import modules.chain_validation as chain_validation
from modules.get_ip import get_local_ip
from client import send_block

difficulty = chain_validation.difficulty
ip_local = get_local_ip()


# Getting the miner's wallet address
wallet_path = 'data/data.json'
try:
    if os.stat(wallet_path).st_size != 0:
        with open('data/data.json') as datafile:
            data = json.load(datafile)
            for d in data['user_data']:
                node_address = d['wallet']
                
except FileNotFoundError:
    print("Missing 'data/data.json' file")
    qui()


def proof_of_work(previous_block):
    new_proof = 1
    check_proof = False
    while check_proof is False:
        hash_operation = hashlib.sha256(str(str(new_proof**2) + json.dumps(previous_block, sort_keys = True)).encode()).hexdigest()
        if hash_operation[:difficulty] == '0'*difficulty:
            check_proof = True
        else:
            new_proof += 1
    return new_proof

def broadcast_block(block):
    with open('data/nodes.json') as nodes_file:
        nodes_data = json.load(nodes_file)
        for d in nodes_data['nodes']:
            addr = d[7:19]
            if addr != ip_local:
                try:
                    send_block(block, addr)
                except ConnectionRefusedError:
                    pass
            else:
                pass



def mine(stop):
    
    with open('data/blockchain.json') as chain_file:
        chain = json.load(chain_file)
    previous_block = chain[-1]
    proof = None
    proof = proof_of_work(previous_block)
    if proof:
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
        chain.append(block)
        with open('data/blockchain.json', 'w') as blockchain_file:
            json.dump(chain, blockchain_file)
        broadcast_block(block)


