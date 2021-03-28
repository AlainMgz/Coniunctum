#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 17:20:24 2021

@author: whip
"""

import socket
import json

def get_local_ip():
	try:
		with open('data.json') as datafile:
			data = json.load(datafile)
			for d in data['user_data']:
				ip_local = d['ip']
			return ip_local
	except FileNotFoundError:
		print("Missing 'data.json' file, please re-install the Client")
	

def get_source_ip():
	try:
		with open('source_data/ip_file.json') as ip_file:
			ip_file = json.load(ip_file)
			for d in ip_file['ip_data']:
				source_ip = d['source_ip']
			return source_ip
	except FileNotFoundError:
		return 'Please get the IP of the source download of the Coniunctum Client'
