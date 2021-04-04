#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 09:46:30 2021

@author: whip
"""

import datetime
from time import sleep
import hashlib
import json
import requests
import curses
from subprocess import call
from uuid import uuid4
from urllib.parse import urlparse
import os
import threading
from first_launch import first_launch_setup
import logging
import pyperclip
from modules.get_ip import get_local_ip
from blockchain import Blockchain
from server import *
from miner import *




# Setting the version of the client

coniunctum_version = "0.1 Alpha"


# Checking if it's the first time the Client is opened
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

first_time_check()
    
# Running a simple wallet ----------------------------------------------------------------------------------------------------

def run_wallet():
    run = True
    print("\nWelcome to the Coniunctum wallet Client")
    while run:
        print(f"\n(Coniunctum {coniunctum_version}) Would you like to :\n\n --> Close the app [1]\n --> Check your balance [2]\n --> Create a transaction [3]\n --> Check your wallet address [4]\n --> Copy wallet address to clipboard [5]\n")
        try:
            input_status = int(input("Input 1, 2, 3, 4 or 5 : "))
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
            else:
                print("\nPlease enter a valid number, retrying...\n")
        except ValueError:
            print("\nPlease enter a valid number, retrying...")
            sleep(2)

# Deploying our Blockchain / Running a full node / miner ---------------------------------------------------------------------
def update_data_live(stop, blockchain, node_address):
    while True:
        if stop():
            break
        try:
            chain = blockchain.chain

            blockchain.scan_local_blockchain()
            blockchain.scan_local_nodes()

            if chain != blockchain.chain:
                who_mined = list(blockchain.chain[-1].values())[2]
                if who_mined == node_address:
                    print("\nYou've mined a block ! The blockchain has been updated, restarting the miner...\n")
                    run_miner = threading.Thread(target=mine, args=(lambda : stop_server_thread,))
                    run_miner.daemon = True
                    run_miner.start()
                else:
                    print("\nBlockchain has been updated.")
            elif chain == blockchain.chain:
                pass


        except ValueError:
            pass

def running_app():
    
    ip_local = get_local_ip()


    # Getting the current node's address

    wallet_path = 'data/data.json'

    try:
        if os.stat(wallet_path).st_size != 0:
            with open('data/data.json') as datafile:
                data = json.load(datafile)
                for d in data['user_data']:
                    node_address = d['wallet']
                    
    except FileNotFoundError:
        print("Missing 'data/data.json' file")
        quit()


    run = True
    print("\nThe Coniunctum Client is starting...\n")
    stop_server_thread = False
    run_server = threading.Thread(target=start, args=(lambda : stop_server_thread,))
    run_server.daemon = True
    run_server.start()


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
    stop_threads = False
    thread = threading.Thread(target=update_data_live, args=(lambda : stop_threads, blockchain, node_address))
    thread.start()
    sleep(2)
    print("\nWelcome to the Coniunctum wallet Client")
    while run:
        
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
                stop_threads = True
                thread.join()
                #server.shutdown(socket.SHUT_RDWR)
                server.close()
                run_miner.join()
                #stop_server = call("shell_scripts/stop_tcp_server.sh", shell=True)
                #stop_miner = call("shell_scripts/stop_miner.sh", shell=True) shouldn't be useful since the miner is ran and stoped in option [6]
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
                    blockchain.scan_replace_chain()
                    print("\nYour node is up and running.\nPress Ctrl+Z then type the 'bg' command to resume the process in the background. You can then close your shell, the node will continue to run.\nTo close the client, kill the coniunctum.py python process.\n")
                    """
                    try:
                        while True:
                            pass
                            #blockchain.scan_local_blockchain()
                            # TO DO : Scan for new transactions and verify them
                    except KeyboardInterrupt:
                        print("\nStopping the node...\n")
                        stop_server = call("shell_scripts/stop_tcp_server.sh", shell=True)
                        sleep(2)
                        pass
                    """
                    sleep(2)
                    os.system('cls' if os.name == 'nt' else 'clear')
                elif role == 3:
                    try:
                        miner_input = int(input("Do you want to run only your node [1] or also your miner [2] ?\nInput --> "))
                    except ValueError:
                        print("Please enter a valid number.")
                    if miner_input == 1:
                        
                        print("\nYour node is up and running, press Ctrl+C to return to the menu (this will stop your node).\nPress Ctrl+Z then type the 'bg' command to resume the process in the background. You can then close your shell, the node will continue to run.\nTo close the client, kill the coniunctum.py python process.\n")
                        """
                        try:
                            while True:
                                chain = blockchain.chain


                                    #blockchain.scan_local_blockchain()
                                    #blockchain.scan_local_nodes()

                                if chain == blockchain.chain:
                                    pass
                                elif chain != blockchain.chain:
                                    print("\nBlockchain has been updated, restarting the miner...")
                                # TO DO : Scan for new transactions and verify them
                        except KeyboardInterrupt:
                            print("\nStopping the node...\n")
                        """    
                        sleep(2)
                        os.system('cls' if os.name == 'nt' else 'clear')
                    elif miner_input == 2:
                        blockchain.scan_replace_chain()
                        run_miner = threading.Thread(target=mine, args=(lambda : stop_server_thread,))
                        run_miner.daemon = True
                        run_miner.start()
                        print("\nYour node and your miner are up and running.\nPress Ctrl+Z then type the 'bg' command to resume the process in the background. You can then close your shell, the node will continue to run.\nTo close the client, kill the coniunctum.py python process.\n")
                        
                        sleep(2)
                        os.system('cls' if os.name == 'nt' else 'clear')
            elif input_status == 7:
                
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
                print("\nPlease enter a valid number, retrying... 1\n")
        except ValueError:
            print("\nPlease enter a valid number, retrying... 2")
            sleep(2)



# Checking if the user need a flask app or not (i.e if the user is just a wallet holder, no need for a flask app)

try:
    with open('data/data.json') as datafile:
        data = json.load(datafile)
        for d in data['user_data']:
            role = d['role']
                
except FileNotFoundError:
    print("Missing 'data/data.json' file")
    quit()

if role == 2 or role == 3:
    running_app()

if role == 1:
    run_wallet()
