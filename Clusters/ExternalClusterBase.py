import socket
import sys
import os
import json
import csv
from collections import namedtuple
from datetime import datetime
import random


TEST_PORT      = 6023#random.randint(4000,9000)
TEST_VARIATION = "default"
TEST_ID 	   = 0
TEST 		   = False

#variation  		= namedtuple('Variation',      'sub_name params_list')


fieldnames = ['id', 'record_time','record_entry_a','record_entry_b','record_entry_c']

#TODO fix this
def get_records(filepath):
	records = []
	with open(filepath) as logfile:
		reader = csv.DictReader(logfile, fieldnames)
		for row in reader:
			#print(row["id"], row["record_entry_a"])
			# TODO namedtuple
			if row["record_entry_a"] and row["record_entry_b"]:
				record = (row["record_entry_b"], row["record_entry_a"])
				print(record)
				records.append((row["record_entry_b"], row["record_entry_a"]))
				#_id = int(row["id"])
	return records

def get_last_record_id(filepath):
	_id = 0
	with open(filepath) as logfile:
		reader = csv.DictReader(logfile, fieldnames)
		for row in reader:
			print(row["id"], row["record_entry_a"])
			if row["id"]:
				_id = int(row["id"])
	return _id+1


def log_responce(filepath, _id, entry_a, entry_b = None, b_required = False, entry_c = None, c_required = False):
	#TODO define it somehow
	#TODO utilize it
	if (b_required and not entry_b) or (c_required and not entry_c):
		return
	fieldnames = ['id', 'record_time','record_entry_a','record_entry_b','record_entry_c']
	empty_entry = lambda _ : _ if _ else "---" 
	with open(filepath, "a") as logfile:
		writer = csv.DictWriter(logfile, fieldnames)
		writer.writerow({"id":str(_id),"record_time":str(datetime.now()), "record_entry_a" : entry_a, "record_entry_b": empty_entry(entry_b), "record_entry_c": empty_entry(entry_c)})



class ExternalCluster():
	def __init__(self, _id, _port, variation):
		self.port        		=  _port
		self._id                =  _id
		self.payload_module     =  None
		self.dispatcher_module  =  None
		#self.set_logics(path_to_configuration, variation)

	def prepare(self, variation):
		...
		#curr_dir = os.getcwd()
		#os.chhdir(path_to_configuration)
		#from cluster import *
		#base_config = os.path.join(path_to_configuration, "config.json")
		#variations  			= self.parse_variations(os.path.join(path_to_configuration, "ideas.json"))
		#self.payload_module 	= PAYLOAD(variations[variation])
		#TODO path to parsing scheme
		#Linguistics etc.
		#self.dispatcher_module  = DISPATCHER()
		#os.chhdir(curr_dir)

	# TODO code duplication with plannerlib
	# fix this
	def parse_variations(self, variations):
		#print("Not error")
		variations = json.load(variations)
		
		variants   = {(_["sub_name"],_["params"]) for _ in variations["variations"]}
		return variants



	def uncover_idea(self, path):
		curr_dir = os.getcwd()
		os.chdir(path)

		base 	   = self.parse_base_idea(open("config.json"))
		#print(base)
		variations = self.parse_variations(open("ideas.json"))

		#sys.path.append(path_to_configuration)
		#from payload     import *
		#self.payload_module = Payload(argv)


	# TODO path to dispatching scheme
	def dispatch(self, request):
		#TODO make it abstract ->> force to write realization
		raise NotImplementedError

	def act(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind(('127.0.0.1', self.port))
			s.listen()
			print("The port is", self.port)
			while True:
				print("Waiting for requests from Violla")
				violla_link, violla_addr = s.accept()
				try:
					with violla_link:
						print("Violla asked for something from ", violla_addr)
						#WHILE CONECTION?
						while True:
							#VIOLLA WILL CLOSE LINK BY HERSELF ON "DONE"
							#TODO be carefull with byte like objects ~ file // picture
							request 			= violla_link.recv(2048).decode()
							print("Violla asked with ", request)
							payload_resolution  = self.dispatch(request)
							print("And module responded with ", payload_resolution)
							violla_link.sendall(payload_resolution.encode(encoding='utf-8'))
				except Exception as e:
					print(e)


	def null_action(self):
		#TODO move to linguistics
		return "Sometimes it's so hard to understand you..."


# if __name__ == '__main__':

# 	#TODO - find a better way to send description to module
# 	_id, port, path_to_configuration, variation = 0, 4047, "/mnt/X/WORKSHOP/Violla/Clusters/Echo", "tweaked"
# 	#_id, port, path_to_configuration, variation = sys.argv[1:5]
# 	cluster = ExternalCluster(_id, port, path_to_configuration, variation)
# 	cluster.act()

