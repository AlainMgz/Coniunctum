#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 23:41:44 2021

@author: whip
"""

import requests
import socket
import json
import pickle
ip_local = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] 
if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), 
s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, 
socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

print(blockchain.nodes)
"""            
try:
    with open('data.json') as data_file:
        data_file = json.load(data_file)
        for d in data_file['first_opening']:
            sender_address = d['wallet']
        input_receiver = input("Please fill in the receiver's address : ")
        input_amount = input(int("PLease enter the amount you want to send : "))
        url = f'http://{ip_local}:5000/add_transaction'
        node_json = {'type': 'p2p',
             'sender': f'{sender_address}',
             'receiver': f'{input_receiver}',
             'amount': f'{input_amount}'
             }
except FileNotFoundError:
    print('Please create and initialize ypurself a wallet')
"""
    

    

                                                       