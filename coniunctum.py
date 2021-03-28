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
from first_launch import first_launch_setup
from blockchain import Blockchain
import logging

# Checking if it's the first time the Client is opened
def first_time_check():
    try:
        with open('need_setup.json') as check_file:
            check_data = json.load(check_file)
            for a in check_data['first_time_open']:
                answer = a['answer']
            if answer == 0:
                setup_res = first_launch_setup()
                if setup_res:
                    pass
                else:
                    quit()
            elif answer == 1:
                pass
            else:
                print("Invalid json data in file 'need_setup.json', if you've changed it manually please revert it to it's original value.")
                quit()
    except FileNotFoundError:
        print("File 'need_setup.json' is missing. Please download it from github and change it to it's last value (if you know it) or reinstall the Client with a new download")
        quit()

first_time_check()
    

# Part 2 - Deploying our Blockchain ---------------------------------------------------------------------


def running_app():
    # Initializing the blockchain

    blockchain = Blockchain()


    # Creating a Web App

    app = Flask(__name__)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

    # Getting the current node's address

    wallet_path = 'data.json'

    try:
        if os.stat(wallet_path).st_size != 0:
            with open('data.json') as datafile:
                data = json.load(datafile)
                for d in data['user_data']:
                    node_address = d['wallet']
                    
    except FileNotFoundError:
        print("Missing 'data.json' file")
        qui()



    # Mining a new block

    @app.route('/mine_block', methods = ['GET'])

    def mine_block():
        previous_block = blockchain.get_previous_block()
        previous_proof = previous_block['proof']
        proof = blockchain.proof_of_work(previous_proof)
        previous_hash = blockchain.hash(previous_block)
        blockchain.mining_reward_transaction(receiver = node_address, amount = 50, proof = proof)
        block = blockchain.create_block(proof, previous_hash)
        response = {'message': 'Congratulations, you just mined a block !',
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'proof': block['proof'],
                    'previous_hash': block['previous_hash'],
                    'transactions': block['transactions']}
        return jsonify(response), 200


    # Getting the full blockchain

    @app.route('/get_chain', methods = ['GET'])

    def get_chain():
        response = {'chain': blockchain.chain,
                    'length': len(blockchain.chain)}
        return jsonify(response), 200


    # Checking if blockchain is valid

    @app.route('/is_valid', methods = ['GET'])

    def is_blockchain_valid():
        is_valid = blockchain.is_chain_valid(blockchain.chain)
        if is_valid:
            response = {'message': 'All good, the Blockchain is valid.'}
        else:
            response = {'message': 'We have a problem, the Blockchain is not valid.'}
        return jsonify(response), 200


    # Adding transactions

    @app.route('/add_transaction', methods = ['POST'])

    def add_transaction():
        json = request.get_json()
        transaction_keys = ['type', 'sender', 'receiver', 'amount']
        if not all (key in json for key in transaction_keys):
            return 'Some elements of the transaction are missing', 400
        index = blockchain.add_transaction(sender = json['sender'], receiver = json['receiver'], amount = json['amount'])
        response = {'message': f'This transaction will be added to Block {index}'}
        return jsonify(response), 201


    # Part 3 - Decentralizing the Blockchain -----------------------------------------------------------------------------------

    # Connecting new nodes

    @app.route('/connect_node', methods = ['POST'])

    def connect_node():
        new_nodes_json = request.get_json()
        nodes = new_nodes_json.get('nodes')
        if nodes is None:
            return 'No nodes', 400
        for node in nodes:
            blockchain.add_node(node)
        json_nodes = {}
        json_nodes['nodes'] = []
        for nodes in blockchain.nodes:
            json_nodes['nodes'].append(nodes)
        with open('nodes.json', 'w') as nodesfile:
            json.dump(json_nodes, nodesfile)
        print('All the nodes are now connected. The Coniunctum Blockchain now contains the following nodes : ')
        print(list(blockchain.nodes))
        return "OK", 201
        
    # Adding a new node to the network

    @app.route('/add_new_node', methods = ['POST'])

    def add_new_node():
        new_node_json = request.get_json()
        node = new_node_json.get('node')
        url = f'{node}/connect_node'
        if node is None:
            return 'No node', 400
        blockchain.add_node(node)
        json_nodes = {}
        json_nodes['nodes'] = []
        for node in blockchain.nodes:
            json_nodes['nodes'].append(node)
        with open('nodes.json', 'w') as nodesfile:
            json.dump(json_nodes, nodesfile)
        r = requests.post(url, json = json_nodes)
        if r.status_code == 201:
            print("Added the new node succesfully !")
            return "OK", 201
        else:
            print("Someting went wrong communicating with the new node")
            return "Something went wrong", 400
        
        
    # Replacing the chain by a longer one

    @app.route('/replace_chain', methods= ['GET'])

    def replace_chain():
        is_chain_replaced = blockchain.scan_replace_chain()
        if is_chain_replaced:
            response = {'message': 'All good, the Blockchain was outdated and is now up to date.',
                        'new_chain': blockchain.chain}
        else:
            response = {'message': 'All good, the Blockchain is up to date.',
                        'current_chain': blockchain.chain}
        return jsonify(response), 200

    # Home page

    @app.route('/')

    def home():
        return "Coniunctum official website ! <a href='/download' download>Download the Coniunctum Client</a><br><a href='/download2' download> DL Source Code</a>"

    # Downloading the client

    @app.route('/download')

    def download_file():
        path = "Coniunctum.zip"
        return send_file(path, as_attachment=True)

    @app.route('/download2')

    def download_file2():
        path = "Coniunctum.py"
        return send_file(path, as_attachment=True)

    # Running the app
    logging.basicConfig(filename='error_main.log',level=logging.DEBUG)

    app.run(host = '0.0.0.0', port = 56230)

running_app()






