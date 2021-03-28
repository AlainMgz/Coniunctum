#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 09:46:30 2021

@author: whip
"""

from flask import Flask, jsonify, request, send_file
import datetime
import hashlib
import json
import requests
import os
import logging
import click

def run_web_client():
    # Creating a Web App
    """
    TO PREVENT ANY OUTPUT FROM FLASK
    def secho(text, file=None, nl=None, err=None, color=None, **styles):
        pass

    def echo(text, file=None, nl=None, err=None, color=None, **styles):
        pass

    click.echo = echo
    click.secho = secho
    """
    logging.basicConfig(filename='error_main.log', level=logging.ERROR)
    """
    TO PREVENT INFO LOGGING
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.WARNING)
    """
    app = Flask(__name__)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

    # Getting the full blockchain

    @app.route('/get_chain', methods = ['GET'])

    def get_chain():
        with open('data/blockchain.json') as chain_file:
            chain = json.load(chain_file)
        response = {'chain': chain,
                        'length': len(chain)}
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
        nodes = set()
        try:
            with open('data/nodes.json') as nodes_file:
                nodes_data = json.load(nodes_file)
                for d in nodes_data['nodes']:
                    nodes.add(d)
        except FileNotFoundError:
                return "Nodes data file missing", 400
        new_nodes_json = request.get_json()
        nodes = new_nodes_json.get('nodes')
        if nodes is None:
            return 'No nodes', 400
        for node in nodes:
            nodes.add(node)
        json_nodes = {}
        json_nodes['nodes'] = []
        for nodes in nodes:
            json_nodes['nodes'].append(nodes)
        with open('data/nodes.json', 'w') as nodesfile:
            json.dump(json_nodes, nodesfile)
        print('All the nodes are now connected. The Coniunctum Blockchain now contains the following nodes : ')
        print(list(nodes))
        return "OK", 201
        
    # Adding a new node to the network

    @app.route('/add_new_node', methods = ['POST'])

    def add_new_node():
        nodes = set()
        try:
            with open('data/nodes.json') as nodes_file:
                nodes_data = json.load(nodes_file)
                for d in nodes_data['nodes']:
                    nodes.add(d)
        except FileNotFoundError:
                return "Nodes data file missing", 400
        new_node_json = request.get_json()
        node = new_node_json.get('node')
        nodes.add(node)
        url = f'{node}/connect_node'
        if node is None:
            return 'No node', 400
        json_nodes = {}
        json_nodes['nodes'] = []
        for node in nodes:
            print(node)
            json_nodes['nodes'].append(node)
        with open('data/nodes.json', 'w') as nodesfile:
            json.dump(json_nodes, nodesfile)
        r = requests.post(url, json = json_nodes)
        if r.status_code == 201:
            print("Added the new node succesfully !")
            print(json_nodes)
            return "OK", 201
        else:
            print("Someting went wrong communicating with the new node")
            return "Something went wrong", 400

    # Home page

    @app.route('/')

    def home():
        return "Coniunctum official website ! <a href='/download' download>Download the Coniunctum Client</a>"

    # Downloading the client

    @app.route('/download')

    def download_file():
        path = "../Coniunctum.zip"
        return send_file(path, as_attachment=True)

    # Running the app
    

    app.run(host = '0.0.0.0', port = 56230)

run_web_client()