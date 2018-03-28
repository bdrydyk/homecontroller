#!/usr/bin/python3
import requests
import csv
import os
import logging
import sched, time
import re, binascii

#ON OFF CCL
BASE_URL = "http://admin:seebeck10@10.0.1.67/"
STATE_STR= "<!-- state=ef lock=e6 -->"

logger = logging.getLogger(__name__)
logger.handlers = []
ch = logging.StreamHandler()
logger.addHandler(ch)
logger.setLevel(logging.INFO)

#bin(int('ff', base=16))[2:]
class WebPowerSwitch(object):
	"""docstring for WebPowerSwitch"""
	def __init__(self):
		super(WebPowerSwitch, self).__init__()
		self.base_url = "http://admin:seebeck10@10.0.1.67/"
		self.outlets = [False,False,False,False,False,False,False,False]
		self.get_outlet_states()
		print("outlet states: {}".format(self.outlets))

	def int_to_bit_list(self,h):
		states = []
		for i in reversed(bin(h)[2:].zfill(8)):
			states.append(bool(int(i)))
		return states

	def str_to_int(self,hex_str):
		return int(hex_str, 16)

	def str_to_bit_list(self,hex_str):
		return self.int_to_bit_list(self.str_to_int(hex_str))

	def get_hex_state(self):
		r = requests.get(self.base_url + 'index.htm')
		m = re.search("<!-- state=(\S\S) lock=(\S\S) -->",r.text)
		print("Hex state: {}".format(m.group(1)))
		return(m.group(1))

	def set_outlet(self,outlet,state):
		if state == True:
			state="ON"
		elif state == False:
			state="OFF"
		print("Setting outlet {}: {}".format(str(outlet),state))
		requests.get(self.base_url + "outlet", params={str(outlet):state})
		return self.get_outlet_states()

	def get_outlet_states(self):
		self.outlets = self.str_to_bit_list(self.get_hex_state())
		return self.outlets

	def set_outlet_states(self,hex_str):
		new_states = self.str_to_bit_list(hex_str)
		current_states = self.get_outlet_states()

		print("current\t\t: {}".format(current_states))
		print("new\t\t: {}".format(new_states))
		
		for i,v in enumerate(new_states):
			v = bool(int(v))
			outlet_num = int(i) + 1
			print("{} == {}".format(bool(current_states[i]), v))
			if v != bool(current_states[i]):
				print("asking outlet num {} to be {}".format(outlet_num,v))
				self.set_outlet(outlet_num,v)
		return(self.get_outlet_states())

	def cycle_outlet_states(self,hex_str):

		swap_states = self.str_to_int(hex_str)
		current_states = self.str_to_int(self.get_hex_state())
		new_states = swap_states ^ current_states
		print("cycle states: {}".format(new_states))
		new_state_str = hex(new_states)[2:]
		res = self.set_outlet_states(new_state_str)
		return(res)

