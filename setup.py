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

def setup():

    ip_local = get_local_ip()


    # Creating the archive directory ---------------------------
    
    directory = "Coniunctum"

    parent_directory = pathlib.Path(__file__).parent.absolute()

    path = os.path.join(parent_directory, directory)

    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    





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

    directory2 = "shell_scripts"

    parent_directory = pathlib.Path(__file__).parent.absolute() / "Coniunctum/"

    path = os.path.join(parent_directory, directory2)

    try:
        os.mkdir(path)
    except FileExistsError:
        pass

    directory2 = "web_app"

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

    need_setup_json = {}
    need_setup_json['first_time_open'] = []
    need_setup_json['first_time_open'].append({"answer": 0})
    with open("Coniunctum/data/need_setup.json", "w") as need_setup:
        json.dump(need_setup_json, need_setup)

    # Copying all the source code ----------------------------------------

    # Copying shell scripts

    shutil.copyfile('shell_scripts/start_miner.sh', 'Coniunctum/shell_scripts/start_miner.sh')
    shutil.copyfile('shell_scripts/start_tcp_server.sh', 'Coniunctum/shell_scripts/start_tcp_server.sh')
    shutil.copyfile('shell_scripts/start_temp.sh', 'Coniunctum/shell_scripts/start_temp.sh')
    shutil.copyfile('shell_scripts/start_web_client.sh', 'Coniunctum/shell_scripts/start_web_client.sh')
    shutil.copyfile('shell_scripts/stop_client.sh', 'Coniunctum/shell_scripts/stop_client.sh')
    shutil.copyfile('shell_scripts/stop_miner.sh', 'Coniunctum/shell_scripts/stop_miner.sh')
    shutil.copyfile('shell_scripts/stop_tcp_server.sh', 'Coniunctum/shell_scripts/stop_tcp_server.sh')
    shutil.copyfile('shell_scripts/stop_temp.sh', 'Coniunctum/shell_scripts/stop_temp.sh')
    shutil.copyfile('shell_scripts/stop_web_client.sh', 'Coniunctum/shell_scripts/stop_web_client.sh')


    # Copying modules

    shutil.copyfile('modules/add_new_node.py', 'Coniunctum/modules/add_new_node.py')
    shutil.copyfile('modules/add_transaction.py', 'Coniunctum/modules/add_transaction.py')
    shutil.copyfile('modules/block_validator.py', 'Coniunctum/modules/block_validator.py')
    shutil.copyfile('modules/chain_validation.py', 'Coniunctum/modules/chain_validation.py')
    shutil.copyfile('modules/get_ip.py', 'Coniunctum/modules/get_ip.py')


    # Copying web app files

    shutil.copyfile('web_app/web_app.py', 'Coniunctum/web_app/web_app.py')
    shutil.copyfile('web_app/web_client.py', 'Coniunctum/web_app/web_client.py')

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
