#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 09:46:30 2021

@author: whip
"""

from flask import Flask, request
import json
import logging

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


# Connecting new nodes

@app.route('/connect_node', methods = ['POST'])

def connect_node():
    new_nodes_json = request.get_json()
    nodes = new_nodes_json.get('nodes')
    if nodes is None:
        return 'No nodes', 400
    with open('data/nodes.json', 'w') as nodesfile:
        json.dump(new_nodes_json, nodesfile)
    return "OK", 201
    
# Home page

@app.route('/')

def home():
    return "This node is in set-up process..."

# Running the app


logging.basicConfig(filename='error.log',level=logging.DEBUG)

app.run(host = '0.0.0.0', port = 56230)