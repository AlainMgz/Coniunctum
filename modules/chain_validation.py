#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 09:46:30 2021

@author: whip
"""

import hashlib
import json

difficulty = 5 #7 for production

# Function that hashes a given block
def hash(block):
    encoded_block = json.dumps(block, sort_keys = True).encode()
    return hashlib.sha256(encoded_block).hexdigest()

# Function that verifies a given blockchain (proofs and hashes)
def is_chain_valid(chain):
    previous_block = chain[0]
    block_index = 1
    while block_index < len(chain):
        block = chain[block_index]
        if block['previous_hash'] != hash(previous_block):
            return False
        proof = block['proof']
        hash_operation = hashlib.sha256(str(str(proof**2) + json.dumps(previous_block, sort_keys = True)).encode()).hexdigest()
        if hash_operation[:difficulty] != '0'*difficulty:
            return False
        previous_block = block
        block_index += 1
    return True