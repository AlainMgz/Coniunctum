#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 17:20:24 2021

@author: whip
"""

import requests
from modules.get_ip import get_local_ip, get_source_ip
import json


# Adding current node to an other node's nodes list

def add_new_full_node(source_ip_arg):

	ip_local = get_local_ip()

	source_ip = source_ip_arg
	
	url = f'http://{source_ip}:56230/add_new_node'
	node_json = {'node': f'http://{ip_local}:56230'}
	try:
		x = requests.post(url, json = node_json)
	except OSError:
		return False
	if x.status_code == 201:
		return True
	else:
		return False



													   




