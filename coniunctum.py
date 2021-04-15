#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 09:46:30 2021
Coniunctum Blockchain
@author: Alain Magazin
"""

import datetime
from time import sleep
import hashlib
import json
from uuid import uuid4
from urllib.parse import urlparse
import os
import threading
import subprocess
from first_launch import first_launch_setup
import pyperclip
from modules.get_ip import get_local_ip, get_source_ip
from blockchain import Blockchain
from server import *
from client import req_blockchain


# Checking if it's the first time the Client is opened using the need_setup.json file (value 0 means it is the first opening)
def first_time_check():
    try:
        with open('data/need_setup.json') as check_file:
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
                print("Invalid json data in file 'data/need_setup.json', if you've changed it manually please revert it to it's original value.")
                quit()
    except FileNotFoundError:
        print("File 'data/need_setup.json' is missing. Please download it from github and change it to it's last value (if you know it) or reinstall the Client with a new download")
        quit()



# Defining the function called in a thread to have live blockchain updates
def update_data_live(stop, blockchain, node_address):
    chain = blockchain.chain
    while True:
        if stop():
            break
        try:
            blockchain.scan_local_blockchain()
            blockchain.scan_local_nodes()
            if chain != blockchain.chain:
                chain = blockchain.chain
                who_mined = list(blockchain.chain[-1].values())[2]
                if who_mined == node_address:
                    print(f"\nYou've mined block {list(blockchain.chain[-1].values())[0]} ! The blockchain has been updated.") 
                else:
                    print("Blockchain has been updated.")
                # If the miner is running we need a way to tell it to stop if someone else mined the current block, so we create a file where we'll store 1 if the miner needs a restart
                # And 0 if it's good to continue. This file is constantly read by the miner the check if it needs to stop.
                need_restart_json = {}
                need_restart_json['need_restart'] = []
                need_restart_json['need_restart'].append({"answer": 1})
                with open("data/miner_restart.json", "w") as miner_restart:
                    json.dump(need_restart_json, miner_restart)
            elif chain == blockchain.chain:
                pass
        except ValueError:
            pass

# Running a simple wallet ----------------------------------------------------------------------------------------------------
# A wallet just needs these 5 basic options
def run_wallet():
    # Setting the version of the client
    coniunctum_version = "0.2 Alpha"
    run = True
    # Starting the TCP server in a seperate thread
    print("The wallet is starting, it might take some time as it needs to sync with the blockchain.")
    source_ip = get_source_ip()
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
        # We need to be able to sync the blockchain, if we can't we close the app
        quit()
    print("\nWelcome to the Coniunctum wallet Client !")
    while run:
        print(
            f"\n(Coniunctum {coniunctum_version}) Would you like to :\n\n --> Close the app [1]\n --> Check your balance [2]\n --> Create a transaction [3]\n --> Check your wallet address [4]\n --> Copy wallet address to clipboard [5]\n --> Sync the blockchain with the network [6]\n")
        try:
            input_status = int(input("Input 1, 2, 3, 4, 5 or 6 : "))
            if input_status == 1:
                run = False
                print("Closing the app...")
            elif input_status == 2:
                print("\nSoon..")
                sleep(3)
            elif input_status == 3:
                print("\nSoon..")
                sleep(3)
            elif input_status == 4:
                with open('data/data.json') as data_file:
                    data = json.load(data_file)
                    for d in data['user_data']:
                        print(f"\nYour wallet address : {d['wallet']}\n")
                sleep(3)
            elif input_status == 5:
                with open('data/data.json') as data_file:
                    data = json.load(data_file)
                    for d in data['user_data']:
                        pyperclip.copy(d['wallet'])  
                print("\nWallet address copied to clipboard !\n")
                sleep(3)
            elif input_status == 6:
                try:
                    req_blockchain(source_ip)
                except ConnectionRefusedError:
                    print("The source node is offline, retry in a few hours or contact the source node operator.")
                    quit()
                print("Blockchain synced.")
            else:
                print("\nPlease enter a valid number, retrying...\n")
        except ValueError:
            print("\nPlease enter a valid number, retrying...")
            sleep(2)

# Deploying our Blockchain / Running a full node / miner ---------------------------------------------------------------------



# Defining the main function
def running_app(role): 
    # Setting the version of the client
    coniunctum_version = "0.2 Alpha"
    # Getting the current node's address
    try:
        with open('data/data.json') as datafile:
            try:
                data = json.load(datafile)
            except json.decoder.JSONDecodeError:
                print("Corrupted 'data/data.json' file")
                quit()
            for d in data['user_data']:
                node_address = d['wallet']              
    except FileNotFoundError:
        print("Missing 'data/data.json' file")
        quit()

    run = True
    print("\nThe Coniunctum Client is starting...\n")

    # Starting the TCP server in a seperate thread
    PORT = 56230
    SERVER = str(get_local_ip())
    ADDR = (SERVER, PORT)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR)
    run_server = threading.Thread(target=start, args=(server, SERVER))
    run_server.daemon = True
    run_server.start()

    #Loading animation (not more useful than sleep() but sleep is needed to wait until the server has started)
    bar = [
    " [=     ]",
    " [ =    ]",
    " [  =   ]",
    " [   =  ]",
    " [    = ]",
    " [     =]",
    " [    = ]",
    " [   =  ]",
    " [  =   ]",
    " [ =    ]",
    ]
    i = 0
    idx = 0
    while i < 3:
        print(bar[idx % len(bar)], end="\r")
        sleep(.1)
        idx += 1
        i += 0.15

    # Initializing the blockchain
    blockchain = Blockchain()

    # Sarting the blockchain update thread
    stop_threads = False
    thread = threading.Thread(target=update_data_live, args=(lambda : stop_threads, blockchain, node_address))
    thread.start()
    sleep(2)
    print("\nWelcome to the Coniunctum wallet Client")
    while run:
        # We check what is the role of the user, output depends on it
        if role == 2: 
            print(f"\n(Coniunctum {coniunctum_version}) Would you like to :\n\n --> Close the app [1]\n --> Check your balance [2]\n --> Create a transaction [3]\n --> Check your wallet address [4]\n --> Copy wallet address to clipboard [5]\n --> Start your node [6]\n --> Sync your blockchain with the network [7]\n")
        elif role == 3:
            print(f"\n(Coniunctum {coniunctum_version}) Would you like to :\n\n --> Close the app [1]\n --> Check your balance [2]\n --> Create a transaction [3]\n --> Check your wallet address [4]\n --> Copy wallet address to clipboard [5]\n --> Start your node and start your miner [6]\n --> Sync your blockchain with the network [7]\n")
        try:
            input_status = int(input("Input 1, 2, 3, 4, 5, 6 or 7 : "))
            if input_status == 1:
                run = False
                # flag variable to print the dots and it's value increases inside the while loop.
                flag = 1
                print("")
                # To print the dots we use while loop. In total, 3 dots will be printed.
                while flag < 4:
                    print("\rClosing the Client" + ("." * flag), end=" ")
                    sleep(1)
                    flag = flag + 1
                print("\n")
                # Stopping the Update and the TCP server threads
                stop_threads = True
                thread.join()
                server.close()
                # Making sure the miner does not need a restart when closing, otherwise it can lead to two miners running on the next run of the client.
                need_restart_json = {}
                need_restart_json['need_restart'] = []
                need_restart_json['need_restart'].append({"answer": 0})
                with open("data/miner_restart.json", "w") as miner_restart:
                    json.dump(need_restart_json, miner_restart)
            elif input_status == 2:
                print("\nSoon..")
                sleep(3)
                os.system('cls' if os.name == 'nt' else 'clear')
            elif input_status == 3:
                print("\nSoon..")
                sleep(3)
                os.system('cls' if os.name == 'nt' else 'clear')
            elif input_status == 4:
                with open('data/data.json') as data_file:
                    data = json.load(data_file)
                    for d in data['user_data']:
                        print(f"\nYour wallet address : {d['wallet']}\n")
                sleep(3)
                os.system('cls' if os.name == 'nt' else 'clear')
            elif input_status == 5:
                with open('data/data.json') as data_file:
                    data = json.load(data_file)
                    for d in data['user_data']:
                        pyperclip.copy(d['wallet'])  
                print("\nWallet address copied to clipboard !\n")
                sleep(3)
                os.system('cls' if os.name == 'nt' else 'clear')
            elif input_status == 6:
                
                sleep(0.5)
                if role == 2:
                    # The user chose to just be a validator, so no miner starting here
                    # First we need to make sure that the node is synced with the network, hence the following line
                    blockchain.scan_replace_chain()
                    blockchain.scan_local_blockchain()
                    print("\nYour node is up and running.\nPress Ctrl+Z then type the 'bg' command to resume the process in the background. You can then close your shell, the node will continue to run.\nTo close the client, kill the coniunctum.py python process.\n")
                    sleep(2)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    # The TCP server handles incoming connections, and the Update thread updates the blockchain when needed
                    # Notining more to do here
                elif role == 3:
                    # We give an option to the user to just run a validator and not a miner
                    miner_input = int(input("Do you want to run only your node [1] or also your miner [2] ?\nInput --> "))
                    if miner_input == 1:
                        # Same as for role == 2
                        blockchain.scan_replace_chain()
                        blockchain.scan_local_blockchain()
                        print("\nYour node is up and running, press Ctrl+C to return to the menu (this will stop your node).\nPress Ctrl+Z then type the 'bg' command to resume the process in the background. You can then close your shell, the node will continue to run.\nTo close the client, kill the coniunctum.py python process.\n") 
                        sleep(2)
                        os.system('cls' if os.name == 'nt' else 'clear')
                    elif miner_input == 2:
                        # As usual, we need to sync to the network
                        blockchain.scan_replace_chain()
                        blockchain.scan_local_blockchain()
                        # We now start the miner in a subprocess (easier to kill than a Thread)
                        run_miner = subprocess.Popen(['python3', 'miner.py', '&'])
                        print("\nYour node and your miner are up and running.\nPress Ctrl+Z then type the 'bg' command to resume the process in the background. You can then close your shell, the node will continue to run.\nTo close the client, kill the coniunctum.py python process.\n")
                        while True:
                            # Here we need a infinite loop to check if the miner needs a restart or not
                            # So for now the client is not usable while the miner is running, have to find a solution for that
                            sleep(0.5)
                            try:
                                # Checking if it needs a restart
                                with open('data/miner_restart.json') as check_file:
                                    check_data = json.load(check_file)
                                for a in check_data['need_restart']:
                                    answer = a['answer']
                                if answer == 0:
                                    pass
                                elif answer == 1:
                                    # We scan our local blockchain (that we know is up to date thanks to the update thread)
                                    # To get the identity of the miner of the last block
                                    blockchain.scan_local_blockchain()
                                    who_mined = list(blockchain.chain[-1].values())[2]
                                    if who_mined == node_address:
                                        # When the miner mines a block it automatically stops so no need to stop it from here
                                        pass
                                    else:
                                        # Here someone else mined the block so we need to manually stop the miner
                                        sleep(0.5)
                                        run_miner.terminate()
                                    # Starting the miner again
                                    sleep(0.5)
                                    run_miner = subprocess.Popen(['python3', 'miner.py', '&'])
                                    print("Restarted the miner.")
                                    # Now that we've restarted the miner, we update the file to tell that it doesn't need a restart anymore
                                    need_restart_json = {}
                                    need_restart_json['need_restart'] = []
                                    need_restart_json['need_restart'].append({"answer": 0})
                                    with open("data/miner_restart.json", "w") as miner_restart:
                                        json.dump(need_restart_json, miner_restart)
                                else:
                                    print("Invalid json data in file 'data/need_setup.json', if you've changed it manually please revert it to it's original value.")
                                    raise KeyboardInterrupt
                            except FileNotFoundError:
                                print("File 'data/miner_restart.json' is missing. Please download it from github and change it to it's last value (if you know it) or reinstall the Client with a new download")
                                raise KeyboardInterrupt
                        sleep(2)
                        os.system('cls' if os.name == 'nt' else 'clear')
            elif input_status == 7:
                # Syncing as usual
                blockchain.scan_local_blockchain()
                print("Syncing with the network...")
                sleep(2)
                replace_chain = blockchain.scan_replace_chain()
                if replace_chain:
                    print("\nBlockchain synced with the network.")
                else:
                    print("\nBlockchain unchanged\n")
                sleep(2)
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                print("\nPlease enter a valid number, retrying...\n")
        except KeyboardInterrupt:
            print("\nPlease enter a valid number (to close the client input 1), retrying...")
            sleep(2)

# Checking what the role of the user and starting the according fucntion -----------------------------
def run():
    first_time_check()
    try:
        with open('data/data.json') as datafile:
            data = json.load(datafile)
            for d in data['user_data']:
                role = d['role']
                    
    except FileNotFoundError:
        print("Missing 'data/data.json' file.")
        quit()

    if role == 2 or role == 3:
        running_app(role)
    elif role == 1:
        run_wallet()
    else:
        print("Corrupted data/data.json file. Please revert to a previous working state.")
