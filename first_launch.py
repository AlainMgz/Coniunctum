#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 09:46:30 2021

@author: whip
"""

import os
from uuid import uuid4
import json
import requests
from subprocess import call
import threading
from time import sleep
from modules.chain_validation import hash, is_chain_valid
from modules.get_ip import get_local_ip, get_source_ip
from setup import setup
from server import *
from client import *

# Defining the main function, it is used to setup the node when it is ran for the first time
def first_launch_setup():
# Check if it's the first time the client is launched, even thaugh we already did that before the function was called
# in coniunctum.py, a double-check is not a luxury
    try:
        with open('data/need_setup.json') as check_file:
            check_data = json.load(check_file)
            for a in check_data['first_time_open']:
                answer = a['answer']
            if answer == 0:
                pass
            elif answer == 1:
                print("This node does not need a setup process, it has already gone through it or the data/need_setup.json was tampered with.")
                return False
            else:
                print("Corrupted data/need_setup.json file. Please revert to previous working state.")
                return False
    except FileNotFoundError:
        print("File 'need_setup.json' is missing. Please download it from github and change it to it's last value (if you know it) or reinstall the Client with a new download")
        return False

    # We create the miner restart file
    need_restart_json = {}
    need_restart_json['need_restart'] = []
    need_restart_json['need_restart'].append({"answer": 0})
    with open("data/miner_restart.json", "w") as miner_restart:
        json.dump(need_restart_json, miner_restart)

    # Get or create the user's data file
    # Even thaugh it should not be already existing as it's the first time opening the client
    # this allows to keep the data if the setup process fails for some reason
    try:
        with open('data/data.json') as datafile:
            data = json.load(datafile)
            for d in data['user_data']:
                node_address = d['wallet']
                name = d['name']
                role = d['role']               
    except FileNotFoundError:
        # We need three pieces of info from the user, his name (really useless for now, can be a pseudonym), his role and his IP address on which the TCP server will listen
        # We also generate a wallet address, later on when we add transacions and digital signatures, key pairs, ... this wallet address will be a hask of the public key
        node_address = str(uuid4()).replace('-', '')
        name = input("Enter your name : ")
        role = int(input("What will your role be in the Coniunctum network (1 : Wallet holder | 2 : Full Node | 3 : Full Node + Miner) : "))
        input_ip = input("Enter the IP address of your node (make sure to read our Network guidelines for more information) : ")
        data = {}
        data['user_data'] = []
        data['user_data'].append({
            'wallet': node_address,
            'name' : name,
            'role' : role,
            'ip' : input_ip
        })
        # We dump this data in a file so it can be reused at any time
        with open('data/data.json', 'w') as datafile:
            json.dump(data, datafile)

    # Seting up the installation archive - This creates a installation archive that can be distributed (see whitepaper for more detail)
    setup()

    # Setup accordingly to the user's role in the network -------------------------------------------------------
    
    # Setup a light node / wallet
    if role == 1:
        # A wallet only needs to be connected to it's source node, so we only add the source node in the data/nodes.json file
        # The source node doesn't need to know about the wallet since it's not going to send data to it, only when the wallet requests and therefore gives it's IP address to the source node
        source_ip = get_source_ip()
        ip_local = get_local_ip()
        json_nodes = {}
        json_nodes['nodes'] = []
        json_nodes['nodes'].append(ip_local)
        json_nodes['nodes'].append(source_ip)
        with open("data/nodes.json", "w") as nodes_file:
            json.dump(json_nodes, nodes_file)
        print("Syncing the blockchain...")
        try:
            # Starting a TCP server to sync the blockchain from the source node
            PORT = 56230
            SERVER = str(get_local_ip())
            ADDR = (SERVER, PORT)
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(ADDR)
            run_server = threading.Thread(target=start, args=(server, SERVER))
            run_server.daemon = True
            run_server.start()
            sleep(2)
            try:
                req_blockchain(source_ip)
            except ConnectionRefusedError:
                print("The source node is offline, retry in a few hours or contact the source node operator.")
                return False
            # Updating the need_setup file
            need_setup_json = {}
            need_setup_json['first_time_open'] = []
            need_setup_json['first_time_open'].append({"answer": 1})
            with open("data/need_setup.json", "w") as need_setup:
                json.dump(need_setup_json, need_setup)
            print("Blockchain is synced, setup is complete. The client will now close and after you will be able to run it normally.")
            server.close()
            return False
        except OSError:
            print("A problem occured running the TCP server.")
            return False

    # Setting up a node / validator
    elif role == 2:
        # Starting the TCP server
        PORT = 56230
        SERVER = str(get_local_ip())
        ADDR = (SERVER, PORT)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(ADDR)
        run_server = threading.Thread(target=start, args=(server, ))
        run_server.daemon = True
        run_server.start()
        sleep(2)
        source_ip = get_source_ip()
        # Retrieving the list of nodes on the network
        try:
            res = req_nodes(source_ip)
        except ConnectionRefusedError:
            print("The source node is offline, retry in a few hours or contact the source node operator.")
            return False
        animation = "|/-\\"
        for i in range(20):
            sleep(0.1)
            print("\r" + animation[i % len(animation)], end=" ")
        if res:
            # Looping through every node to tell them about this new node
            with open("data/nodes.json") as nodes_file:
                nodes_data = json.load(nodes_file)
            for n in nodes_data['nodes']:
                ip_local = get_local_ip()
                if n != ip_local:
                    if n != source_ip:
                        try:
                            req_nodes(n)
                        except ConnectionRefusedError:
                            pass
            print("Synced nodes succesfully")
            print("Syncing the blockchain...")
            with open("data/nodes.json") as nodes_file:
                nodes_data = json.load(nodes_file)
            # Looping through every node and requesting their blockchain
            for n in nodes_data['nodes']:
                ip_local = get_local_ip()
                if n != ip_local:
                    try:
                        req_blockchain(n)
                        animation = "|/-\\"
                        for i in range(20):
                            sleep(0.1)
                            print("\r" + animation[i % len(animation)], end=" ")
                        try:
                            with open("data/blockchain.json"):
                                pass
                        except FileNotFoundError:
                            print("Blockchain not updated...")
                            return False
                    except OSError:
                        pass
                else:
                    pass
            server.close()
            # TO DO : Analyze the blockchain to get the wallet's balance
            # Updating the need_setup file
            need_setup_json = {}
            need_setup_json['first_time_open'] = []
            need_setup_json['first_time_open'].append({"answer": 1})
            with open("data/need_setup.json", "w") as need_setup:
                json.dump(need_setup_json, need_setup)
            print("Blockchain is synced, setup is complete. The client will now turn off and you will be able to start it normally rigth after.")
            return False
        else:
            print("Something went wrong connecting to the Coniunctum network. Maybe the source client is offline")
            return False
            
    # Setting up the full node (node + miner)
    elif role == 3:
        # More or less the same as with the simple node (role == 2)
        PORT = 56230
        SERVER = str(get_local_ip())
        ADDR = (SERVER, PORT)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(ADDR)
        run_server = threading.Thread(target=start, args=(server, SERVER))
        run_server.daemon = True
        run_server.start()
        sleep(2)
        print("Syncing nodes...")
        source_ip = get_source_ip()
        try:
            res = req_nodes(source_ip)
        except ConnectionRefusedError:
            print("The source node is offline, retry in a few hours or contact the source node operator.")
            return False
        animation = "|/-\\"
        for i in range(20):
            sleep(0.1)
            print("\r" + animation[i % len(animation)], end=" ")
        if res:
            with open("data/nodes.json") as nodes_file:
                nodes_data = json.load(nodes_file)
            for n in nodes_data['nodes']:
                ip_local = get_local_ip()
                if n != ip_local:
                    if n != source_ip:
                        req_nodes(n)
            print("Synced nodes succesfully")
            print("\nSyncing the blockchain...")
            with open("data/nodes.json") as nodes_file:
                nodes_data = json.load(nodes_file)
            for n in nodes_data['nodes']:
                ip_local = get_local_ip()
                if n != ip_local:
                    try:
                        req_blockchain(n)
                        animation = "|/-\\"
                        for i in range(20):
                            sleep(0.1)
                            print("\r" + animation[i % len(animation)], end=" ")
                        try:
                            with open("data/blockchain.json"):
                                pass
                        except FileNotFoundError:
                            print("Blockchain not updated...")
                            return False
                    except OSError:
                        pass
                else:
                    pass
            server.close()
            # TO DO : Analyze the blockchain to get the wallet's balance
            need_setup_json = {}
            need_setup_json['first_time_open'] = []
            need_setup_json['first_time_open'].append({"answer": 1})
            with open("data/need_setup.json", "w") as need_setup:
                json.dump(need_setup_json, need_setup)
            print("Blockchain is synced, setup is complete. The client will now turn off and you will be able to start it normally rigth after.\n")
            return False
            

        else:
            print("Something went wrong connecting to the Coniunctum network. Maybe the source client is offline")
            return False


