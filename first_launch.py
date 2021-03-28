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
from time import sleep
from chain_validation import hash, is_chain_valid
from add_new_node import add_new_full_node
from get_ip import get_local_ip, get_source_ip
from setup import setup


def first_launch_setup():

# Change shell script permissions
	os.chmod('./start_client.sh', 0o774)
	os.chmod('./stop_client.sh', 0o774)

#Check if it's the first time the client is launched

	try:
		with open('need_setup.json') as check_file:
			check_data = json.load(check_file)
			for a in check_data['first_time_open']:
				answer = a['answer']
			if answer == 0:
				pass
			elif answer == 1:
				print("Internal Error")
				return False
			else:
				print("Internal Error 2")
				return False
	except FileNotFoundError:
		print("File 'need_setup.json' is missing. Please download it from github and change it to it's last value (if you know it) or reinstall the Client with a new download")
		return False


# Get or create the user's data file

	wallet_path = 'data.json'

	try:
		if os.stat(wallet_path).st_size != 0:
			with open('data.json') as datafile:
				data = json.load(datafile)
				for d in data['user_data']:
					node_address = d['wallet']
					name = d['name']
					role = d['role']
					
	except FileNotFoundError:
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
		with open('data.json', 'w') as datafile:
			json.dump(data, datafile)

# Seting up the installation archive 

	setup()


# Setup accordingly to the user's role in the network
	
	# Setup a light node aka a wallet
	if role == 1:
		ip_local = get_local_ip()
		source_ip = get_source_ip()
		json_nodes = {}
		json_nodes['nodes'] = []
		json_nodes['nodes'].append(f"http://{ip_local}:56230")
		json_nodes['nodes'].append(f"http://{source_ip}:56230")
		source_node = f"http://{source_ip}:56230"
		with open("nodes.json", "w") as nodes_file:
			json.dump(json_nodes, nodes_file)
		print("Syncing the blockchain...")
		try:
			req = requests.get(f"{source_node}/get_chain")
			if req.status_code == 200:
				chain = req.json()['chain']
				with open("blockchain.json", "w") as blockchain_file:
					json.dump(chain, blockchain_file)
				# TO BE DONE : Analyze the blockchain to get the wallet's balance
				need_setup_json = {}
				need_setup_json['first_time_open'] = []
				need_setup_json['first_time_open'].append({"answer": 1})
				with open("need_setup.json", "w") as need_setup:
					json.dump(need_setup_json, need_setup)
				print("Blockchain is synced, setup is complete. The client will now run normally.")
				return True
				
			else:
				print(f"Couldn't sync the blockchain, http error code : {req.status_code}")
				return False
		except OSError:
			print("The source client is offline")
			return False


	elif role == 2:
		run_temp_app = call("./start_client.sh", shell=True)
		sleep(5)
		res = add_new_full_node()
		if res:
			stp_temp_app = call("./stop_client.sh", shell=True)
			print("Synced nodes succesfully")
			print("Syncing the blockchain...")
			longest_chain = None
			max_length = 0
			with open("nodes.json") as nodes_file:
				nodes_data = json.load(nodes_file)
				for n in nodes_data['nodes']:
					ip_local = get_local_ip()
					if n != f"http://{ip_local}:56230":
						try:
							req_chain = requests.get(f'{n}/get_chain')
							if req_chain.status_code == 200:
								length = req_chain.json()['length']
								chain = req_chain.json()['chain']
								if length > max_length and is_chain_valid(chain):
									max_length = length
									longest_chain = chain
								else:
									pass
							else:
								pass
						except OSError:
							pass
					else:
						pass
			if longest_chain:
				with open("blockchain.json", "w") as chain_file:
					json.dump(longest_chain, chain_file)
			else:
				return False
			# TO BE DONE : Analyze the blockchain to get the wallet's balance
			need_setup_json = {}
			need_setup_json['first_time_open'] = []
			need_setup_json['first_time_open'].append({"answer": 1})
			with open("need_setup.json", "w") as need_setup:
				json.dump(need_setup_json, need_setup)
			print("Blockchain is synced, setup is complete. The client will now turn off and you will be able to start it normally rigth after.")
			return False
						

		else:
			print("Something went wrong connecting to the Coniunctum network. Maybe the source client is offline")
			return False

	elif role == 3:
		run_temp_app = call("./start_client.sh", shell=True)
		sleep(5)
		res = add_new_full_node()
		if res:
			stp_temp_app = call("./stop_client.sh", shell=True)
			print("Synced nodes succesfully")
			print("Syncing the blockchain...")
			longest_chain = None
			max_length = 0
			with open("nodes.json") as nodes_file:
				nodes_data = json.load(nodes_file)
				for n in nodes_data['nodes']:
					ip_local = get_local_ip()
					if n != f"http://{ip_local}:56230":
						try:
							req_chain = requests.get(f'{n}/get_chain')
							if req_chain.status_code == 200:
								length = req_chain.json()['length']
								chain = req_chain.json()['chain']
								if length > max_length and is_chain_valid(chain):
									max_length = length
									longest_chain = chain
								else:
									pass
							else:
								pass
						except OSError:
							pass
					else:
						pass
			if longest_chain:
				with open("blockchain.json", "w") as chain_file:
					json.dump(longest_chain, chain_file)
			else:
				return False
			# TO BE DONE : Analyze the blockchain to get the wallet's balance
			need_setup_json = {}
			need_setup_json['first_time_open'] = []
			need_setup_json['first_time_open'].append({"answer": 1})
			with open("need_setup.json", "w") as need_setup:
				json.dump(need_setup_json, need_setup)
			print("Blockchain is synced, setup is complete. The client will now turn off and you will be able to start it normally rigth after.")
			return False
			

		else:
			print("Something went wrong connecting to the Coniunctum network. Maybe the source client is offline")
			return False


