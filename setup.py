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
from get_ip import get_local_ip

def setup():

    ip_local = get_local_ip()


    f = open('ip_file.json', 'w')
    f.write('{"ip_data": [{"source_ip": "' + ip_local + '"}]}')
    f.close()

    directory = "Coniunctum"

    parent_directory = pathlib.Path(__file__).parent.absolute()

    path = os.path.join(parent_directory, directory)

    try:
        os.mkdir(path)
    except FileExistsError:
        pass

    directory = "source_data"

    parent_directory = pathlib.Path(__file__).parent.absolute() / 'Coniunctum'

    path = os.path.join(parent_directory, directory)

    try:
        os.mkdir(path)
    except FileExistsError:
        pass


    shutil.copyfile(pathlib.Path(__file__).parent.absolute() / 'setup.py', pathlib.Path(__file__).parent.absolute() / 'setup2.py')
    shutil.copyfile(pathlib.Path(__file__).parent.absolute() / 'coniunctum.py', pathlib.Path(__file__).parent.absolute() / 'coniunctum2.py')
    shutil.copyfile(pathlib.Path(__file__).parent.absolute() / 'add_new_node.py', pathlib.Path(__file__).parent.absolute() / 'add_new_node2.py')
    shutil.copyfile(pathlib.Path(__file__).parent.absolute() / 'add_transaction.py', pathlib.Path(__file__).parent.absolute() / 'add_transaction2.py')
    shutil.copyfile(pathlib.Path(__file__).parent.absolute() / 'blockchain.py', pathlib.Path(__file__).parent.absolute() / 'blockchain2.py')
    shutil.copyfile(pathlib.Path(__file__).parent.absolute() / 'chain_validation.py', pathlib.Path(__file__).parent.absolute() / 'chain_validation2.py')
    shutil.copyfile(pathlib.Path(__file__).parent.absolute() / 'first_launch.py', pathlib.Path(__file__).parent.absolute() / 'first_launch2.py')
    shutil.copyfile(pathlib.Path(__file__).parent.absolute() / 'get_ip.py', pathlib.Path(__file__).parent.absolute() / 'get_ip2.py')
    shutil.copyfile(pathlib.Path(__file__).parent.absolute() / 'need_setup.json', pathlib.Path(__file__).parent.absolute() / 'need_setup2.json')
    shutil.copyfile(pathlib.Path(__file__).parent.absolute() / 'start_client.sh', pathlib.Path(__file__).parent.absolute() / 'start_client2.sh')
    shutil.copyfile(pathlib.Path(__file__).parent.absolute() / 'stop_client.sh', pathlib.Path(__file__).parent.absolute() / 'stop_client2.sh')
    shutil.copyfile(pathlib.Path(__file__).parent.absolute() / 'web_app.py', pathlib.Path(__file__).parent.absolute() / 'web_app2.py')

    try:
        shutil.move(pathlib.Path(__file__).parent.absolute() / "ip_file.json", pathlib.Path(__file__).parent.absolute() / "Coniunctum/source_data/ip_file.json")
    except FileNotFoundError:
        pass

    try:
        shutil.move(pathlib.Path(__file__).parent.absolute() / "setup2.py", pathlib.Path(__file__).parent.absolute() / "Coniunctum/setup2.py")
    except FileNotFoundError:
        pass

    try:
        shutil.move(pathlib.Path(__file__).parent.absolute() / "coniunctum2.py", pathlib.Path(__file__).parent.absolute() / "Coniunctum/coniunctum2.py")
    except FileNotFoundError:
        pass

    try:
        shutil.move(pathlib.Path(__file__).parent.absolute() / "add_new_node2.py", pathlib.Path(__file__).parent.absolute() / "Coniunctum/add_new_node2.py")
    except FileNotFoundError:
        pass

    try:
        shutil.move(pathlib.Path(__file__).parent.absolute() / "add_transaction2.py", pathlib.Path(__file__).parent.absolute() / "Coniunctum/add_transaction2.py")
    except FileNotFoundError:
        pass

    try:
        shutil.move(pathlib.Path(__file__).parent.absolute() / "blockchain2.py", pathlib.Path(__file__).parent.absolute() / "Coniunctum/blockchain2.py")
    except FileNotFoundError:
        pass

    try:
        shutil.move(pathlib.Path(__file__).parent.absolute() / "chain_validation2.py", pathlib.Path(__file__).parent.absolute() / "Coniunctum/chain_validation2.py")
    except FileNotFoundError:
        pass

    try:
        shutil.move(pathlib.Path(__file__).parent.absolute() / "first_launch2.py", pathlib.Path(__file__).parent.absolute() / "Coniunctum/first_launch2.py")
    except FileNotFoundError:
        pass

    try:
        shutil.move(pathlib.Path(__file__).parent.absolute() / "get_ip2.py", pathlib.Path(__file__).parent.absolute() / "Coniunctum/get_ip2.py")
    except FileNotFoundError:
        pass

    try:
        shutil.move(pathlib.Path(__file__).parent.absolute() / "need_setup2.json", pathlib.Path(__file__).parent.absolute() / "Coniunctum/need_setup2.json")
    except FileNotFoundError:
        pass

    try:
        shutil.move(pathlib.Path(__file__).parent.absolute() / "start_client2.sh", pathlib.Path(__file__).parent.absolute() / "Coniunctum/start_client2.sh")
    except FileNotFoundError:
        pass

    try:
        shutil.move(pathlib.Path(__file__).parent.absolute() / "stop_client2.sh", pathlib.Path(__file__).parent.absolute() / "Coniunctum/stop_client2.sh")
    except FileNotFoundError:
        pass

    try:
        shutil.move(pathlib.Path(__file__).parent.absolute() / "web_app2.py", pathlib.Path(__file__).parent.absolute() / "Coniunctum/web_app2.py")
    except FileNotFoundError:
        pass



    old_name_coniunctum = pathlib.Path(__file__).parent.absolute() / "Coniunctum/coniunctum2.py"
    new_name_coniunctum = pathlib.Path(__file__).parent.absolute() / "Coniunctum/coniunctum.py"
    os.rename(old_name_coniunctum, new_name_coniunctum)

    old_name_setup = pathlib.Path(__file__).parent.absolute() / "Coniunctum/setup2.py"
    new_name_setup = pathlib.Path(__file__).parent.absolute() / "Coniunctum/setup.py"
    os.rename(old_name_setup, new_name_setup)

    old_name_add_new_node = pathlib.Path(__file__).parent.absolute() / "Coniunctum/add_new_node2.py"
    new_name_add_new_node = pathlib.Path(__file__).parent.absolute() / "Coniunctum/add_new_node.py"
    os.rename(old_name_add_new_node, new_name_add_new_node)

    old_name_add_new_transaction = pathlib.Path(__file__).parent.absolute() / "Coniunctum/add_transaction2.py"
    new_name_add_new_transaction = pathlib.Path(__file__).parent.absolute() / "Coniunctum/add_transaction.py"
    os.rename(old_name_add_new_transaction, new_name_add_new_transaction)

    old_name = pathlib.Path(__file__).parent.absolute() / "Coniunctum/blockchain2.py"
    new_name = pathlib.Path(__file__).parent.absolute() / "Coniunctum/blockchain.py"
    os.rename(old_name, new_name)

    old_name = pathlib.Path(__file__).parent.absolute() / "Coniunctum/chain_validation2.py"
    new_name = pathlib.Path(__file__).parent.absolute() / "Coniunctum/chain_validation.py"
    os.rename(old_name, new_name)

    old_name = pathlib.Path(__file__).parent.absolute() / "Coniunctum/first_launch2.py"
    new_name = pathlib.Path(__file__).parent.absolute() / "Coniunctum/first_launch.py"
    os.rename(old_name, new_name)

    old_name = pathlib.Path(__file__).parent.absolute() / "Coniunctum/get_ip2.py"
    new_name = pathlib.Path(__file__).parent.absolute() / "Coniunctum/get_ip.py"
    os.rename(old_name, new_name)

    old_name = pathlib.Path(__file__).parent.absolute() / "Coniunctum/need_setup2.json"
    new_name = pathlib.Path(__file__).parent.absolute() / "Coniunctum/need_setup.json"
    os.rename(old_name, new_name)

    old_name = pathlib.Path(__file__).parent.absolute() / "Coniunctum/start_client2.sh"
    new_name = pathlib.Path(__file__).parent.absolute() / "Coniunctum/start_client.sh"
    os.rename(old_name, new_name)

    old_name = pathlib.Path(__file__).parent.absolute() / "Coniunctum/stop_client2.sh"
    new_name = pathlib.Path(__file__).parent.absolute() / "Coniunctum/stop_client.sh"
    os.rename(old_name, new_name)

    old_name = pathlib.Path(__file__).parent.absolute() / "Coniunctum/web_app2.py"
    new_name = pathlib.Path(__file__).parent.absolute() / "Coniunctum/web_app.py"
    os.rename(old_name, new_name)

    shutil.make_archive("Coniunctum", 'zip', "Coniunctum")

    os.remove(parent_directory / 'setup.py')
    os.remove(parent_directory / 'coniunctum.py')
    os.remove(parent_directory / 'add_new_node.py')
    os.remove(parent_directory / 'add_transaction.py')
    os.remove(parent_directory / 'source_data/ip_file.json')
    os.remove(parent_directory / 'blockchain.py')
    os.remove(parent_directory / 'chain_validation.py')
    os.remove(parent_directory / 'first_launch.py')
    os.remove(parent_directory / 'get_ip.py')
    os.remove(parent_directory / 'need_setup.json')
    os.remove(parent_directory / 'start_client.sh')
    os.remove(parent_directory / 'stop_client.sh')
    os.remove(parent_directory / 'web_app.py')
    os.rmdir(parent_directory / 'source_data')
    os.rmdir(pathlib.Path(__file__).parent.absolute() / 'Coniunctum')
    #os.remove(pathlib.Path(__file__).parent.absolute() / 'setup.py')



