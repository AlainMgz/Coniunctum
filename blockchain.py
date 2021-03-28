#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 09:46:30 2021

@author: whip
"""

import datetime
import hashlib
import json
from flask import Flask, jsonify, request, send_file
import requests
from uuid import uuid4
from urllib.parse import urlparse
import os
import socket
from get_ip import get_local_ip
import chain_validation

class Blockchain:
    
    difficulty = chain_validation.difficulty
    
    def __init__(self):
        
        ip_local = get_local_ip()
        self.chain = []
        self.transactions = []
        self.nodes = set()
        self.scan_local_nodes()
        self.scan_local_blockchain()
    
    def scan_local_nodes(self):
        try:
            with open('nodes.json') as nodes_file:
                nodes_data = json.load(nodes_file)
                for d in nodes_data['nodes']:
                    self.add_node(d)
            print("Nodes network of current blockchain : ")
            print(self.nodes)
        except FileNotFoundError:
                return "Nodes data file missing"

    def scan_local_blockchain(self):
        try:
            with open("blockchain.json") as chain_file:
                chain = json.load(chain_file)
                self.chain = chain
        except FileNotFoundError:
            return "Blockchain data file missing"
                                                       
        
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        with open('blockchain.json', 'w') as blockchain_file:
            json.dump(self.chain, blockchain_file)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:self.difficulty] == '0'*self.difficulty:
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:self.difficulty] != '0'*self.difficulty:
                return False
            previous_block = block
            block_index += 1
        return True
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'type': 'p2p',
                                  'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    def mining_reward_transaction(self, receiver, amount, proof):
        previous_block = self.get_previous_block()
        previous_proof = previous_block['proof']
        hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
        if hash_operation[:self.difficulty] == '0'*self.difficulty:
            self.transactions.append({'type': 'reward',
                                      'receiver': receiver,
                                      'amount': amount})
            previous_block = self.get_previous_block()
            return previous_block['index'] + 1
        else:
            return False
    
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(f'http://{parsed_url.netloc}')

    def replace_chain(self, chain):
        self.chain = chain
        with open('blockchain.json', 'w') as blockchain_file:
            json.dump(self.chain, blockchain_file)
        return True
        
    def scan_replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            if node != f'http://{self.ip_local}:56230':
                try:
                    response = requests.get(f'{node}/get_chain')
                    if response.status_code == 200:
                        length = response.json()['length']
                        chain = response.json()['chain']
                        if length > max_length and self.is_chain_valid(chain):
                            max_length = length
                            longest_chain = chain
                        else:
                            pass
                    else:
                        print(f"Couldn't retrieve the blockchain from this node : {node}")
                        pass
                except OSError:
                    print(f"This node is offline : {node}")
                    pass
            else:
                pass
        if longest_chain:
            return self.replace_chain(longest_chain)
        return False

