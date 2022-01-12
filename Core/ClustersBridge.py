# port = 4078
import socket
import time
import json
import threading

class ExternalLink():
	def __init__(self, port):
		self.port = port
		self.actor = self.act()
		#TODO to config
		self.max_retry = 5
		# TODO fix cross-links
		next(self.actor)




	def act(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			while s.connect_ex(("127.0.0.1", self.port)) != 0:
				time.sleep(2)
				self.max_retry-=1
				if not self.max_retry:
					raise Exception("Cluster was not launched, or whatever, anyway socket is unavaliable.")
			#s.connect(('127.0.0.1', self.port))
			print("Bridge port is", self.port)
			while True:
				req = yield
				print("Asking for send", req)
				s.sendall(req.encode(encoding='utf-8'))
				resp = s.recv(2048).decode()
				#data = json.loads(resp)
				#print("Responded with", data["message"])
				yield resp

	

class InternalLink():
	def __init__(self, port, form_callback, cluster):
		self.port 				= port
		self.actor     			= self.act()

		self.max_retry 			= 5
		self.form_idea_callback = form_callback
		self.cluster = cluster

		self.server 			= threading.Thread(target=self.server_thread)
		self.server.start()
		self.income_queue = []
		self.outcome_queue = []
		#self.detach_idea_callback = detach_callback
		next(self.actor)

	# TODO Make this Asynch
	#Start in thread with callback
	def act(self):
		#TODO fix synchronisation. Overall.
		while True:
			message = yield
			self.income_queue.append(message)
			while not self.outcome_queue:
				time.sleep(1)
			yield self.outcome_queue.pop()
		#while True
		#message = yield
		#self.form_idea_callback(message)

		#cluster_link, cluster_addr = s.accept()
		#return cluster_link, cluster_addr

	# first message goes to violla as idea description from callback
	# next schemene
	# message = yield
	# send do thread
	# yeld thread responce
	#
	# on done
	# done callback
	# somehow close connection
	# restart rhread // connection // listen
	def server_thread(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind(('127.0.0.1', self.port))
			s.listen()
			while True:
				print("Waiting for requests from Clusters")
				cluster_link, cluster_addr = s.accept() #s.accept()
				# TODO bad parameters processing
				#self, cluster, idea_type = IDEA_TYPE.NEW, idea_direction = IDEA_DIRECTION.COVER, inner_memory = ""
				try:
					with cluster_link:
						print("Cluster asked for something from ", cluster_addr)
						request 			= cluster_link.recv(2048).decode()
						print("get request")
						self.form_idea_callback(self.cluster, inner_memory = request)
						while True:
							while not self.income_queue:
								time.sleep(1)
							violla_responce = self.income_queue.pop()
							cluster_link.sendall(violla_responce.encode(encoding='utf-8'))
							request 			= cluster_link.recv(2048).decode()
							data 				= json.loads(request)
							print("Responded with", data["message"])
							self.outcome_queue.append(request)
							# TODO it's op for Violla to decide on
							if "done" in data["type"].lower():
								cluster_link.shutdown(socket.SHUT_WR)
								cluster_link.close()
								break
							
				except Exception as e:
					print(e)




class ClusterDescription():
	def __init__(self):
		self._port = None
		self._id = None
		# TODO set all to properties
		self.name = None
		self._keywords = []
		self.link = None
		self.controller = None
		self.callback = None

	@property
	def port(self):
		return self._port

	@port.setter
	def port(self, val):
		self._port = val

	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, val):
		self._id = id


	@property
	def keywords(self):
		return self._keywords

	def add_keyword(self, new_key):
		self.keywords.append(new_key)

	# TODO fix bad naming
	def set_link(self, _type=None, link=None, callback=None):
		if link:
			self.link = link
		else:
			self.set_remote_link(_type, callback)

	def set_remote_link(self, _type, callback):
		if _type == "External":
			self.link = ExternalLink(self.port)
		else:
			#TODO Can use other cluster as idea handler
			#Don't know why do such a thing
			self.link = InternalLink(self.port, self.callback, self)
			#raise Exception("Add processing of internal motives")
		#self.port


	def set_controller(self, controller):
		self.controller = controller

	# TODO change to some sort of more direct logics
	# TODO do something with default parameters
	def register_as_idea(self, idea_type, idea_direction, inner_memory=""):
		self.controller.register_idea(self, idea_type, idea_direction, inner_memory)

	def set_callback(self, callback):
		self.callback = callback
