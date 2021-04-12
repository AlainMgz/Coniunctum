#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 09:46:30 2021

@author: whip
"""

import datetime
import hashlib
import json
from uuid import uuid4
from urllib.parse import urlparse
import os
import socket
from modules.get_ip import get_local_ip
import modules.chain_validation as chain_validation
from client import req_blockchain


# Defining the blockchain class
class Blockchain:
    
    difficulty = chain_validation.difficulty
    
    
    def __init__(self):
        # Initializing the blockchain, especially syncing the blockchain with the rest of the network
        self.ip_local = get_local_ip()
        self.chain = []
        self.transactions = []
        self.nodes = set()
        self.scan_local_nodes()
        self.scan_local_blockchain()
        self.scan_replace_chain()
        print("This client is connected to these nodes : ")
        print(self.nodes)
    
    # Method to get the nodes from the local file and put them in the blockchain.nodes attribute
    def scan_local_nodes(self):
        try:
            with open('data/nodes.json') as nodes_file:
                nodes_data = json.load(nodes_file)
                for d in nodes_data['nodes']:
                    self.nodes.add(d)
        except FileNotFoundError:
                return "Nodes data file missing"

    # Method to get the blockchain from the local file and put it in the blockchain.chain attribute
    def scan_local_blockchain(self):
        try:
            with open("data/blockchain.json") as chain_file:
                chain = json.load(chain_file)
                if chain != self.chain:
                    self.chain = chain
                else:
                    pass
        except FileNotFoundError:
            return "Blockchain data file missing"
                                                       
    # Method to get the last block of the chain
    def get_previous_block(self):
        return self.chain[-1]
    
    # Method to compute the proof of work of the next block
    def proof_of_work(self, previous_block):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(str(new_proof**2) + json.dumps(previous_block, sort_keys = True)).encode()).hexdigest()
            if hash_operation[:self.difficulty] == '0'*self.difficulty:
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    # Method to hash a given block
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    # Method to verify if a given chain is valid (i.e verify if the hashes link well and if the proofs of each blockare indeed valid)
    # When transactions come this also needs to verify if each block is valid or not
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            proof = block['proof']
            hash_operation = hashlib.sha256(str(str(proof**2) + json.dumps(previous_block, sort_keys = True)).encode()).hexdigest()
            if hash_operation[:self.difficulty] != '0'*self.difficulty:
                return False
            previous_block = block
            block_index += 1
        return True
    
    # Method to add a transaction, useless for now and might be done differently in the future
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'type': 'p2p',
                                  'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    # Method to create the miner's reward transaction that is automatically added to the block that he mined
    def mining_reward_transaction(self, receiver, amount, proof):
        previous_block = self.get_previous_block()
        hash_operation = hashlib.sha256(str(str(proof**2) + json.dumps(previous_block, sort_keys = True)).encode()).hexdigest()
        if hash_operation[:self.difficulty] == '0'*self.difficulty:
            self.transactions.append({'type': 'reward',
                                      'receiver': receiver,
                                      'amount': amount})
            previous_block = self.get_previous_block()
            return previous_block['index'] + 1
        else:
            return False
    
    # Method to replace the chain in the local file with the chain contained in the blockchain.chain attribute
    def replace_chain(self, chain):
        self.chain = chain
        with open('data/blockchain.json', 'w') as blockchain_file:
            json.dump(self.chain, blockchain_file)
        return True

    # Method to scan the network of nodes for their blockchains    
    def scan_replace_chain(self):
        network = self.nodes
        for node in network:
            addr = node
            if addr != self.ip_local:
                try:
                    req_blockchain(addr)
                    return True
                except (OSError, ConnectionRefusedError, ConnectionResetError):
                    pass
            else:
                pass
        return False

