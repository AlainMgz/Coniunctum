#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 18:54:26 2021

@author: whip
"""

import json
import os
import pathlib
import shutil
import requests
import socket
from modules.get_ip import get_local_ip

# The function that creates the installer archive that can be distributed
def setup():
    # Get the machine's local IP
    ip_local = get_local_ip()

    # Creating the archive directory ---------------------------
    directory = "Coniunctum"
    parent_directory = pathlib.Path(__file__).parent.absolute()
    path = os.path.join(parent_directory, directory)
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    
    # Creating the needed directories for the Coniunctum Client
    directory2 = "source_data"
    parent_directory = pathlib.Path(__file__).parent.absolute() / "Coniunctum/"
    path = os.path.join(parent_directory, directory2)
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

    directory2 = "data"
    parent_directory = pathlib.Path(__file__).parent.absolute() / "Coniunctum/"
    path = os.path.join(parent_directory, directory2)
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

    directory2 = "modules"
    parent_directory = pathlib.Path(__file__).parent.absolute() / "Coniunctum/"
    path = os.path.join(parent_directory, directory2)
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

    # Creating the source IP file
    f = open('Coniunctum/source_data/ip_file.json', 'w')
    f.write('{"ip_data": [{"source_ip": "' + ip_local + '"}]}')
    f.close()

    # Creating the need_setup file
    need_setup_json = {}
    need_setup_json['first_time_open'] = []
    need_setup_json['first_time_open'].append({"answer": 0})
    with open("Coniunctum/data/need_setup.json", "w") as need_setup:
        json.dump(need_setup_json, need_setup)

    # Copying all the source code ----------------------------------------

    # Copying modules
    shutil.copyfile('modules/add_transaction.py', 'Coniunctum/modules/add_transaction.py')
    shutil.copyfile('modules/block_validator.py', 'Coniunctum/modules/block_validator.py')
    shutil.copyfile('modules/chain_validation.py', 'Coniunctum/modules/chain_validation.py')
    shutil.copyfile('modules/get_ip.py', 'Coniunctum/modules/get_ip.py')


    # Copying root files
    shutil.copyfile('blockchain.py', 'Coniunctum/blockchain.py')
    shutil.copyfile('client.py', 'Coniunctum/client.py')
    shutil.copyfile('coniunctum.py', 'Coniunctum/coniunctum.py')
    shutil.copyfile('first_launch.py', 'Coniunctum/first_launch.py')
    shutil.copyfile('miner.py', 'Coniunctum/miner.py')
    shutil.copyfile('server.py', 'Coniunctum/server.py')
    shutil.copyfile('setup.py', 'Coniunctum/setup.py')

    #Copying requirements.txt
    shutil.copyfile('requirements.txt', 'Coniunctum/requirements.txt')

    # Create the archive ----------------------------------------------------
    shutil.make_archive("Coniunctum", 'zip', "Coniunctum")

    # Delete the temp folder
    shutil.rmtree('Coniunctum/')
