import socket
import sys
import json
import csv
from collections import namedtuple
from datetime import datetime
import os

TEST_VIOLLA_PORT    = 4073
#TEST_CLUSTER_PORT   = 4075
TEST_CLUSTER_ID	    = 0
TEST_CLUSTER_CONFIG	= "default"
stream_TO_violla        = "/tmp/TEST_PIPE_TO"
stream_FROM_violla      = "/tmp/TEST_PIPE_FROM"
TEST 				= True


#TODO integrate it
#log_record = namedtuple("log_record", 'id record_time record_entry_a record_entry_b record_entry_c')

# >>> with open('names.csv', newline='') as csvfile:
# ...     reader = csv.DictReader(csvfile)
# ...     for row in reader:
# ...         print(row['first_name'], row['last_name'])


# TODO move this and a lot of other logics into clusterlib // ClusterCore != CoreCluster
fieldnames = ['id', 'record_time','record_entry_a','record_entry_b','record_entry_c']

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



class InternalCluster():
	#TODO fix code duplication with this and External Cluster
	def __init__(self, _id, violla_port, variation, link_to_violla = None, link_from_violla = None):
		self.violla_port        = violla_port
		self._stream_to 				= stream_TO_violla
		self._stream_from 			    = stream_FROM_violla
		self._id                = _id
		self.variation 			= variation
		self.active_payload     = self.payload()
		next(self.active_payload)
		#self.set_logics(path_to_configuration, argv)

	#def set_logics(self, path_to_configuration, argv):
	#	sys.path.append(path_to_configuration)
	#	from payload     import *
	#	self.payload_module = Payload(argv)

	def payload(self):

		raise NotImplementedError

	# TODO path to dispatching scheme
	def dispatch(self, request):
		#TODO make it abstract ->> force to write realization
		#self.dispatcher.dispatch(request)
		raise NotImplementedError

	def act(self):
		if os.path.exists(self._stream_to):
			os.remove(self._stream_to)
		if os.path.exists(self._stream_from):
			os.remove(self._stream_from)
		os.mkfifo(self._stream_to)
		os.mkfifo(self._stream_from)
		for idea in self.active_payload:
			try:
				stream_to   = os.open(self._stream_to, os.O_SYNC | os.O_CREAT | os.O_RDWR)
				stream_from = os.open(self._stream_from, os.O_RDONLY)
				#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:stream_to
				#with os.open(self._stream_to, os.O_SYNC | os.O_CREAT | os.O_RDWR) as stream_to, os.open(self._stream_from, os.O_RDONLY) as stream_from:
				#	s.connect(('127.0.0.1', self.violla_port))

				while True:
					os.write(stream_to, idea.encode(encoding='UTF-8'))
					violla_responce = os.read(stream_from, 2048).decode()
					idea = self.dispatch(violla_responce)
						#VIOLLA WILL CLOSE LINK BY HERSELF ON "DONE"
				#		s.sendall(idea.encode(encoding='UTF-8'))
						#violla_responce = ""
						#while True:
				#		violla_responce = s.recv(2048).decode()
						#violla_responce+=responce_part
						#if not responce_part:
						#break
							#violla_responce     =   
						#if not violla_responce:
						#	continue

				#		print("violla say", violla_responce)
						# TODO make version not requiring direct send call

					idea 				= self.dispatch(violla_responce)
			except Exception as e:
				print(e)

    # TODO make it all part of some abstract cluster
	def null_action(self, *args):
		#TODO move to linguistics
		return "Sometimes it's so hard to understand you..."




